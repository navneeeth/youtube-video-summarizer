from flask import jsonify
from config import db 

def get_status_from_db(status_obj):
    doc_ref = db.collection(u'auth').document(status_obj.ack_id)
    status_data = doc_ref.get().to_dict()
    
    if 'status' in status_data:
        status_obj.status = status_data['status']
    else:
        status_obj.status = 'Error: Status not found'
        
    return status_obj

def validate_request_data(data):
    ack_id = data.get('ackId')

    if ack_id is None:
        return jsonify({'status': 'error', 'message': 'ackId parameter is missing'})

    if not isinstance(ack_id, str):
        return jsonify({'status': 'error', 'message': 'ackId parameter must be a string'})

    return None  # No validation errors, return None to indicate success
