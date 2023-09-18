from flask import request, jsonify
from helpers.title.title_helpers import *

def route_get_title():
    video_link = request.args.get('videoLink')
    title_info = fetch_video_title(video_link)
    
    return jsonify(title_info)