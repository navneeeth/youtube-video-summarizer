from flask import jsonify
from config import db

def get_summary_from_db(summary_obj):
    doc_ref = db.collection(u'auth').document(summary_obj.ack_id)
    summary_data = doc_ref.get().to_dict()
    
    if 'summary' in summary_data:
        summary_obj.summary = summary_data['summary']
    else:
        summary_obj.summary = 'Error: Status not found'
        
    return summary_obj

def validate_request_data(data):
    ack_id = data.get('ackId')

    if ack_id is None:
        return jsonify({'status': 'error', 'message': 'ackId parameter is missing'})

    if not isinstance(ack_id, str):
        return jsonify({'status': 'error', 'message': 'ackId parameter must be a string'})

    return None  # No validation errors, return None to indicate success