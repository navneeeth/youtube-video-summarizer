from flask import request, jsonify
from helpers.status.status_helpers import *
from models.status.status_model import Status

def route_get_status():
    # Get the acknowledgment ID from the JSON request
    request_data = request.get_json()
    
    # Validate the request data
    validation_result = validate_request_data(request_data)
    if validation_result:
        return validation_result
    
    ack_id = request_data.get('ackId')

    # Create an instance of the Status class
    status_obj = Status(ack_id, '')
    
    # Call the function to retrieve and update the status
    status_obj = get_status_from_db(status_obj)
    
    # Check if the status is an error message
    if 'Error' in status_obj.status:
        return jsonify({'status': 'error', 'message': status_obj.status})

    # Access the updated status
    status = status_obj.status

    # Return the status
    return jsonify({
        'status': status
    })