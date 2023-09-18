from flask import request, jsonify
from helpers.summary.summary_helpers import *
from models.summary.summary_model import Summary

def route_get_summary():
    request_data = request.get_json()
    
    # Validate the request data
    validation_result = validate_request_data(request_data)
    if validation_result:
        return validation_result
    
    # Get the acknowledgment ID from the JSON request
    ack_id = request_data.get('ackId')
    
    # Create an instance of the Status class
    summary_obj = Summary(ack_id, '')
    
    # Call the function to retrieve and update the status
    summary_obj = get_summary_from_db(summary_obj)
    
    # Check if the status is an error message
    if 'Error' in summary_obj.summary:
        return jsonify({'status': 'error', 'message': summary_obj.summary})

    # Access the updated status
    summary = summary_obj.summary

    # Return the status
    return jsonify({
        'status': 'success',
        'message': summary
    })    
    