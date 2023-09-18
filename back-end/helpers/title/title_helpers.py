from validators import url as is_valid_url
import requests

def fetch_video_title(video_link):
    if not is_valid_url(video_link):
        return {'status': 'error', 'message': 'Please enter a valid YouTube link'}
    
    response = requests.get(f'https://www.youtube.com/oembed?url={video_link}&format=json')
    
    if response.ok:
        print('Response ok')
        title = response.json()['title']
        return {'status': 'success', 'message': title}
    else:
        return {'status': 'error', 'message': 'Could not retrieve video title'}