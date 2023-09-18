from flask import jsonify
import openai

def validate_openai_id(openai_id):
    try:
        openai.api_key = openai_id
        models = openai.Model.list()
        return {'status': 'success'}
    except Exception as e:
        return {'status': 'error', 'message': str(e)}
    
def validate_request_data(openai_id):
    if not openai_id:
        return jsonify({'status': 'error', 'message': 'OpenAI ID is missing'})

    if not isinstance(openai_id, str):
        return jsonify({'status': 'error', 'message': 'OpenAI ID must be a string'})

    return None  # No validation error