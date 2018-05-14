import requests
import json


def parse_response(response):
    result = None
    try:
        parsed_json = json.loads(response.content.decode())
        if 'result' in parsed_json:
            result = parsed_json['result']['lyric_text']
        return result

    except Exception as e:
        print('Parsing json failed :', e) 
        return None


def fetch_lyric(artist, title):
    try:
        response = requests.get('http://94.102.59.115/api/v1/?mus={0}&artist={1}'.format(title, artist))
        print(artist, ' ', title, 'response code: ', response.status_code)
        return response
    except requests.ConnectionError as e:
        print(artist, ' ', title, 'Fetching failed :', e)
        raise
    except Exception as e:
        return None


def get_lyric(artist, title):
    result = None
    try:
        response = fetch_lyric(artist, title)
    except requests.ConnectionError as e:
        return (None, "Check your network connection.")
    if response is not None:
        result = parse_response(response)
    if result is not None:
        result += "\n\n Lyric source: genius.com"
    return (result, None)
    
