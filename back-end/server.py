from flask import Flask, request, jsonify
import openai
import requests
from flask_cors import CORS
from validators import url as is_valid_url
from controllers.id.id_controller import route_get_id
from controllers.status.status_controller import route_get_status
from controllers.summary.summary_controller import route_get_summary
from controllers.openai.openai_controller import route_validate_openai_id
from config import db

app = Flask(__name__)
CORS(app)

@app.after_request
def add_header(response):
    response.headers['X-Frame-Options'] = 'ALLOW-FROM *'
    return response

@app.route('/')
def hello():
    return "Hello!"

# Route to get the id of a task that has begun processing
app.add_url_rule('/get-id', methods=['POST'], view_func=route_get_id)

# Route to get the status of the processing task
app.add_url_rule('/get-status', methods=['POST'], view_func=route_get_status)

# Route to get the summary of the processed task
app.add_url_rule('/get-summary', methods=['POST'], view_func=route_get_summary)

# Route to validate the OpenAI ID
app.add_url_rule('/validate-openai-id', methods=['POST'], view_func=route_validate_openai_id)

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
    