# youtube-video-summarizer

Developed a YouTube Video Summarizer based on GPT-3.5-turbo and Whisper API by OpenAI. 
Validates YouTube link and OpenAI API Key, downloads the video, transcribes the video's audio, and summarizes the content. 
Frontend on HTML, CSS, and JS. 
Backend uses Firebase NoSQL Cloud Firestore database, Python Flask, Whisper API, gpt-3.5-turbo, pytube, etc. 
Interaction uses RESTful APIs.
Check the app out at: https://padaki-n.com/youtube-video-summarizer/

## Code structure:

Directory| Description
--- | ---
front-end | Contains the code for the front-end hosted [here](https://padaki-n.com/youtube-video-summarizer/). The *scipt.js* contains the JavaScript logic for processing the front-end in *index.html* styled with *style.css*. |
back-end | Contains the code (*server.py*) for the back-end logic to process RESTful API requests with error-handling from the front-end to validate input, interact with the Cloud Firestore NoSQL database, download the video, convert to audio, audio transcription, and summarization. We connect to Firebase by creating an API Key as a JSON file named *videosummarizergpt.json*. The backend follows a Model-Controller approach in handling the routes.  