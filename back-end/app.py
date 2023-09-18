from flask import Flask
from controllers.id.id_controller import route_get_id

app = Flask(__name__)

app.add_url_rule('/get-id', methods=['POST'], view_func=route_get_id)

if __name__ == '__main__':
    app.run(debug=True)