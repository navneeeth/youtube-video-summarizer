from flask import request, jsonify
from helpers.openai.openai_helpers import *

def route_validate_openai_id():
    openai_id = request.form['openai-id']
    
    # Validate the request_data
    validation_result = validate_request_data(openai_id)
    if validation_result:
        return validation_result

    # Validate the openai_id
    validation_result = validate_openai_id(openai_id)
    
    return jsonify(validation_result)