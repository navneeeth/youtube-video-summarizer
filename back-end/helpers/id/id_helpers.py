from flask import jsonify
import random
import string
from config import db

def generate_random_id(length=15):
    """
    Generate a random ID with numbers and letters.
    Args:
        length (int): The length of the generated ID (default is 15).
    Returns:
        str: The random ID.
    """
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def check_id_exists(new_id):
    """
    Check if the ID already exists in the Firestore collection.
    Args:
        new_id (str): The ID to check.
    Returns:
        bool: True if the ID exists, False otherwise.
    """
    id_doc = db.collection('auth').document(new_id).get()
    return id_doc.exists

def store_id(id_data):
    """
    Store the ID data in the Firestore collection.
    Args:
        id_data (dict): Data to be stored in Firestore.
    Returns:
        bool: True if the data was successfully stored, False otherwise.
    """
    try:
        db.collection('auth').document(id_data['acknowledgement_id']).set(id_data)
        return True
    except Exception as e:
        print(f"Error in storing ID data: {str(e)}")
        return False

def validate_request_data(request_data):
    timestamp = request_data.get('timestamp')
    video_link = request_data.get('videoLink')
    video_title = request_data.get('videoTitle')

    # Validate the timestamp (required)
    if timestamp is None:
        return jsonify({'status': 'error', 'message': 'Timestamp is required'}), 400

    # Validate the video link (string)
    if not isinstance(video_link, str):
        return jsonify({'status': 'error', 'message': 'Video link must be a string'}), 400

    # Validate the video title (string)
    if not isinstance(video_title, str):
        return jsonify({'status': 'error', 'message': 'Video title must be a string'}), 400

    # If all validations pass, return None (indicating no errors)
    return None

