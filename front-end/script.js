//const apiUrl = "https://yt-video-summarizer-backend.herokuapp.com";
const apiUrl = "http://127.0.0.1:5000";
var formattedTitle = '';
function previewVideo() {
    const videoLink = document.getElementById("video-link").value;
    const iframe = document.getElementById("video-iframe");
    const title = document.getElementById("video-title");
    var thumbnailUrl = '';
    
    var thumbnail;
    
    


    const openaiId = document.getElementById("openai-id").value;
    if (videoLink == "" || openaiId == "") {
        alert("Please enter both a YouTube video link and an OpenAI API key.");
      } 

    // Set the src attribute of the iframe to the entered video link
    iframe.setAttribute("src", videoLink);
    // if(validateOpenAIID(openaiId) == true) 

  validateOpenAIID(openaiId).then(result => {
    if (result) {
        // continue with video summary process
        console.log('OpenAI ID is valid');
         // Make an API call to get the video title
    fetch(`${apiUrl}/get-title?videoLink=${videoLink}`)
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Display the video preview and title
            document.getElementById("status-text").innerHTML = "";
            document.getElementById("status").style.display = "none";
            iframe.setAttribute('src', `https://www.youtube.com/embed/${videoLink.substring(videoLink.lastIndexOf('/') + 1)}`);
            document.getElementById("video-preview").style.display = "block";
            formattedTitle = data.message.replace(/\s+/g, "_");
            // Remove special characters
            formattedTitle = formattedTitle.replace(/[^\w\s]/gi, "");
            title.innerHTML = data.message;
            console.log(title.innerHTML);
            
        } else {
            // Display an error message
            document.getElementById("status-text").innerHTML = "Please enter a valid YouTube link";
            document.getElementById("status").style.display = "block";
        }
    })
    .catch(error => {
        // Display an error message
        document.getElementById("status-text").innerHTML = "An error occurred while getting the video title. Please try again later.";
        document.getElementById("status").style.display = "block";
    });
    } else {
        // handle OpenAI ID validation error
    }
});

        
  
   
}

function goBack() {
    // Hide the video preview and show the form again
    document.getElementById("video-preview").style.display = "none";
    document.getElementById("status").style.display = "none";
}

/*
function continueProcess() {
    // Show the loading status and make an API call to get the video summary
    document.getElementById("status-text").innerHTML = "Loading...";
    document.getElementById("status").style.display = "block";
    const videoLink = document.getElementById("video-link").value;
    //const videoTitle = document.getElementById("video-title").innerHTML;
    var videoTitle = formattedTitle;
    const timestamp = Date.now();
    
    fetch(`${apiUrl}/get-id`, {
        method: "POST",
        body: JSON.stringify({
            videoLink: videoLink,
            videoTitle: videoTitle,
            timestamp: timestamp
        }),
        headers: {
            "Content-type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Call the 'get-status' API every 3 seconds
            const ackId = data.ack_id;
            console.log('success in get id');
            console.log(ackId);
            let interval = setInterval(() => {
                fetch(`${apiUrl}/get-status?ackId=${ackId}`)
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById("status-text").innerHTML = data.status;
                        if (data.status === "Ready") {
                            clearInterval(interval);
                            fetch(`${apiUrl}/get-summary?ackId=${ackId}`)
                                .then(response => response.json())
                                .then(data => {
                                    if (data.status === "success") {
                                        // Display the video summary
                                        document.getElementById("status").style.display = "none";
                                        document.getElementById("result-text").innerHTML = data.message;
                                        document.getElementById("result").style.display = "block";
                                    } else {
                                        // Display an error message
                                        document.getElementById("status-text").innerHTML = "An error occurred while getting the video summary.";
                                    }
                                })
                                .catch(error => {
                                    // Display an error message
                                    document.getElementById("status-text").innerHTML = "An error occurred while getting the video summary.";
                                });
                        } else if (data.status === "Error") {
                            console.log("Error in status of get id");
                            clearInterval(interval);
                            // Display an error message
                            document.getElementById("status-text").innerHTML = "An error occurred while processing the video.";
                        }
                    })
                    .catch(error => {
                        console.log("Error in catch of get status");
                        clearInterval(interval);
                        // Display an error message
                        document.getElementById("status-text").innerHTML = "An error occurred while checking the status.";
                    });
            }, 3000);
        } else {
            // Display an error message
            console.log("Error in else success false of get id");
            document.getElementById("status-text").innerHTML = "An error occurred while processing the video.";
        }
    })
    .catch(error => {
        // Display an error message
        console.log("Error in catch of get id");
        document.getElementById("status-text").innerHTML = "An error occurred while processing the video.";
    });
}
*/

function continueProcess() {
    // Show the loading status and make an API call to get the video summary
    document.getElementById("status-text").innerHTML = "Loading...";
    document.getElementById("status").style.display = "block";
    const videoLink = document.getElementById("video-link").value;
    //const videoTitle = document.getElementById("video-title").innerHTML;
    var videoTitle = formattedTitle;
    const timestamp = Date.now();
    
    fetch(`${apiUrl}/get-id`, {
        method: "POST",
        body: JSON.stringify({
            videoLink: videoLink,
            videoTitle: videoTitle,
            timestamp: timestamp
        }),
        headers: {
            "Content-type": "application/json"
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "success") {
            // Call the 'get-status' API every 3 seconds
            const ackId = data.ack_id;
            console.log('success in get id');
            console.log(ackId);
            let interval = setInterval(() => {
                fetch(`${apiUrl}/get-status`, {
                    method: "POST",
                    body: JSON.stringify({
                        ackId: ackId
                    }),
                    headers: {
                        "Content-type": "application/json"
                    }
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById("status-text").innerHTML = data.status;
                    if (data.status === "Ready") {
                        clearInterval(interval);
                        fetch(`${apiUrl}/get-summary`, {
                            method: "POST",
                            body: JSON.stringify({
                                ackId: ackId
                            }),
                            headers: {
                                "Content-type": "application/json"
                            }
                        })
                        .then(response => response.json())
                        .then(data => {
                            if (data.status === "success") {
                                // Display the video summary
                                document.getElementById("status").style.display = "none";
                                document.getElementById("result-text").innerHTML = data.message;
                                document.getElementById("result").style.display = "block";
                            } else {
                                // Display an error message
                                document.getElementById("status-text").innerHTML = "An error occurred while getting the video summary.";
                            }
                        })
                        .catch(error => {
                            // Display an error message
                            document.getElementById("status-text").innerHTML = "An error occurred while getting the video summary.";
                        });
                    } else if (data.status === "Error") {
                        console.log("Error in status of get id");
                        clearInterval(interval);
                        // Display an error message
                        document.getElementById("status-text").innerHTML = "An error occurred while processing the video.";
                    }
                })
                .catch(error => {
                    console.log("Error in catch of get status");
                    clearInterval(interval);
                    // Display an error message
                    document.getElementById("status-text").innerHTML = "An error occurred while checking the status.";
                });
            }, 3000);
        } else {
            // Display an error message
            console.log("Error in else success false of get id");
            document.getElementById("status-text").innerHTML = "An error occurred while processing the video.";
        }
    })
    .catch(error => {
        // Display an error message
        console.log("Error in catch of get id");
        document.getElementById("status-text").innerHTML = "An error occurred while processing the video.";
    });
}



function validateOpenAIID(openaiId) {
    return fetch(`${apiUrl}/validate-openai-id`, {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: `openai-id=${openaiId}`
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // Continue with video summary process
            console.log('success validating open ai id');
            return true;
        } else {
            alert('OpenAI ID invalid');
            return false;
        }
    })
    .catch(error => {
        console.log('An error occurred while validating OpenAI ID', error);
        alert('An error occurred while validating OpenAI ID. Please try again later.');
        return false;
    });
}


