import requests
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import sys
import pprint

def parse_response(response):
    try:
        result = json.loads(str(response.content, 'utf-8'))['mus'][0]['text']
        return result
    except Exception as e:
        print('Parsing Json failed', e)
        return None

def fetch_lyric(artist, title):
    try:
        response = requests.get(
            'http://api.vagalume.com.br/search.php?art={0}&mus={1}'.format(artist, title))
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
        response = fetch_lyric(artist.split(';')[0], title)
    except requests.ConnectionError as e:
        return (None, "Check your network connection.")
    if response is not None:
        result = parse_response(response)
    else:
        return (None, "Some error happend")
    if result is not None:
        result += "\n\n Lyric source: chartlyrics.com"
    return (result, None)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print("main")
        art = sys.argv[1]
        mus = sys.argv[2]
        response = fetch_lyric(art, mus)
        result = json.loads(str(response.content, 'utf-8'))['mus'][0]['text']
        print(result)
