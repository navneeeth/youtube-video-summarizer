from flask import Flask, request, jsonify
import random
import string
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import moviepy.editor as mp
import openai
from pytube import YouTube
import threading
import requests
from flask_cors import CORS
from validators import url as is_valid_url
from controllers.id.id_controller import route_get_id
from controllers.status.status_controller import route_get_status
from config import db

app = Flask(__name__)
CORS(app)
MAX_THREADS = 5
active_threads = []

'''
# Initialize Firebase credentials and Firestore client
cred = credentials.Certificate('assets/videosummarizergpt.json')
firebase_admin.initialize_app(cred)
db = firestore.client()
'''

def get_id():
    request_data = request.get_json()
    timestamp = request_data.get('timestamp')
    video_link = request_data.get('videoLink')
    video_title = request_data.get('videoTitle')
    acknowledgement_id = None

    while not acknowledgement_id:
        # Generate a random 15-character ID with numbers and letters
        new_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=15))

        # Check if the ID already exists in the Firestore collection
        id_doc = db.collection('auth').document(new_id).get()
        if not id_doc.exists:
            # If the ID is unique, store it in the Firestore collection
            db.collection('auth').document(new_id).set({'timestamp': timestamp, 'status': 'Acknowledged', 'video_link': video_link, 'video_title': video_title, 'summary': ''})
            acknowledgement_id = new_id
    #data = [new_id, timestamp, video_link, video_title]
    start_processing(new_id, timestamp, video_link, video_title)
    # Return the acknowledgement ID to the user
    print(acknowledgement_id)
    return jsonify({
        'ack_id': acknowledgement_id,
        'status': 'success'
    })
    


def process_request(new_id, timestamp, video_link, video_title):
    print('Started thread')
    print(threading.current_thread().name)
    db.collection('auth').document(new_id).set({'timestamp': timestamp, 'status': 'Downloading', 'video_link': video_link, 'video_title': video_title, 'summary': ''})
    video_file = video_title + ".mp4"
    audio_file = video_title + ".mp3"
    updated_audio_file = "updated_" + audio_file
    youtube = YouTube(video_link, use_oauth=True, allow_oauth_cache=True)
    print(youtube)
    audio = youtube.streams.filter(only_audio=True).first()
    audio.download(filename=video_file)
    # convert the downloaded audio file to mp3 format
    mp.AudioFileClip(video_file).write_audiofile(audio_file)
    print("Processing finished for timestamp:", timestamp, "and video link:", video_link)
    db.collection('auth').document(new_id).set({'timestamp': timestamp, 'status': 'Transcribing', 'video_link': video_link, 'video_title': video_title, 'summary': ''})
    # transcribe the audio using OpenAI's API
    file = open(audio_file, "rb")
    transcription = openai.Audio.transcribe("whisper-1", file)

    # write the transcription to a text file
    with open(video_title+"_transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription["text"])
    db.collection('auth').document(new_id).set({'timestamp': timestamp, 'status': 'Summarizing', 'video_link': video_link, 'video_title': video_title, 'summary': ''})
    prompt = "Organize this transcription from a YouTube video into a structured set of easily understandable points without missing important details: "+transcription["text"]
    summary = openai.ChatCompletion.create(
        model="gpt-3.5-turbo", 
        messages=[{"role": "user", "content": prompt}]
    )
    text = ""
    print(summary.choices)
    if len(summary.choices) > 0:
        text = summary.choices[0].message.content
        print(text)
    else:
        print("Error: No response generated.")
        db.collection('auth').document(new_id).set({'timestamp': timestamp, 'status': 'Error', 'video_link': video_link, 'video_title': video_title, 'summary': ''})
    # print the summary and write it to a text file
    with open(video_title+"_summary.txt", "w") as f:
        f.write(text)
    db.collection('auth').document(new_id).set({'timestamp': timestamp, 'status': 'Ready', 'video_link': video_link, 'video_title': video_title, 'summary': text})
    os.remove(video_title+"_summary.txt")
    os.remove(video_title+"_transcription.txt")
    os.remove(video_file)
    os.remove(audio_file)
    active_threads.stop()

def start_processing(new_id, timestamp, video_link, video_title):
    global active_threads
    # Check if there are already MAX_THREADS active threads
    if len(active_threads) >= MAX_THREADS:
        # Wait for one of the threads to complete
        active_threads[0].join()
        # Remove the completed thread from the list
        active_threads = active_threads[1:]
    # Create a new thread for the request
    t = threading.Thread(target=process_request, args=(new_id, timestamp, video_link, video_title))
    # Add the thread to the list of active threads
    active_threads.append(t)
    # Start the thread
    t.start()

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'ALLOW-FROM *'
    return response

@app.route('/')
def hello():
    return "Hello!"


app.add_url_rule('/get-id', methods=['POST'], view_func=route_get_id)

# Route to get the status of the processing task
app.add_url_rule('/get-status', methods=['POST'], view_func=route_get_status)

'''
@app.route('/get-status', methods=['POST'])
def get_status():
    # Get the acknowledgment ID from the JSON request
    data = request.get_json()
    ack_id = data.get('ackId')

    # Retrieve the status from Firebase
    doc_ref = db.collection(u'auth').document(ack_id)
    status = doc_ref.get().to_dict()['status']

    # Return the status
    return jsonify({
        'status': status
    })
'''

# Route to get the summary of the processed task
@app.route('/get-summary', methods=['POST'])
def get_summary():
    # Get the acknowledgment ID from the JSON request
    data = request.get_json()
    ack_id = data.get('ackId')
    
    # Retrieve the status from Firebase
    doc_ref = db.collection(u'auth').document(ack_id)
    summary = doc_ref.get().to_dict()['summary']
    
    # Return the status
    return jsonify({
        'status': 'success',
        'message': summary
    })

@app.route('/validate-openai-id', methods=['POST'])
def validate_openai_id():
    openai_id = request.form['openai-id']
    print(openai_id)
    try:
        openai.api_key = openai_id
        models = openai.Model.list()
        #print(models)
        #print(type(models))
    
        print('success')
        return jsonify({'status': 'success'})

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/get-title')
def get_title():
    video_link = request.args.get('videoLink')
    if not is_valid_url(video_link):
        print('Invalid YouTube link:', video_link)
        return jsonify({'status': 'error', 'message': 'Please enter a valid YouTube link'})
    
    response = requests.get(f'https://www.youtube.com/oembed?url={video_link}&format=json')
    if response.ok:
        print('Valid YouTube link:', video_link)
        title = response.json()['title']
        return jsonify({'status': 'success', 'message': title})
    else:
        print('Invalid YouTube link:', video_link)
        return jsonify({'status': 'error', 'message': 'Could not retrieve video title'})


# Example usage
if __name__ == '__main__':
    app.run()
    