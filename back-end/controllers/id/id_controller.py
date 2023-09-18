from helpers.id.id_helpers import *
from helpers.video_processing.video_processing_helpers import start_processing_thread
from models.id.id_model import ID
from flask import request, jsonify

def route_get_id():
    request_data = request.get_json()
    
    # Validate the request data
    validation_result = validate_request_data(request_data)
    if validation_result:
        return validation_result
    
    timestamp = request_data.get('timestamp')
    video_link = request_data.get('videoLink')
    video_title = request_data.get('videoTitle')
    acknowledgement_id = None

    acknowledgement_id = None

    while not acknowledgement_id:
        # Generate a random 15-character ID with numbers and letters
        new_id = generate_random_id()

        # Check if the ID already exists in the Firestore collection
        if not check_id_exists(new_id):
            # If the ID is unique, create an instance of the ID class
            id_data = ID(
                acknowledgement_id=new_id,
                timestamp=timestamp,
                video_link=video_link,
                video_title=video_title,
                summary='',
                status='Acknowledged'
            )

            if store_id(id_data.__dict__):
                acknowledgement_id = new_id
                # Start the processing thread after storing the ID
                start_processing_thread(new_id, timestamp, video_link, video_title)
            else:
                # Return an error if store_id fails
                return jsonify({'status': 'error', 'message': 'Failed to store ID'})

    # Return the acknowledgement ID to the user
    return jsonify({
        'ack_id': acknowledgement_id,
        'status': 'success'
    })