from flask import Flask
from flask_cors import CORS
from controllers.id.id_controller import route_get_id
from controllers.status.status_controller import route_get_status
from controllers.summary.summary_controller import route_get_summary
from controllers.openai.openai_controller import route_validate_openai_id
from controllers.title.title_controller import route_get_title

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

# Route to get the YouTube video title from the link
app.add_url_rule('/get-title', methods=['GET'], view_func=route_get_title)

# Example usage
if __name__ == '__main__':
    app.run()
    