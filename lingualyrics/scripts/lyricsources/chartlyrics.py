import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from xml.etree import ElementTree
import sys


def parse_response(response):
    try:
        tree = ElementTree.fromstring(response.content)
        print(response)
        result = tree.find('{http://api.chartlyrics.com/}Lyric').text
        return result

    except Exception as e:
        print('Parsing xml failed :', e) 
        return None


def fetch_lyric(artist, title):
    try:
        response = requests.get('http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect\
                        ?artist={0}&song={1}'.format(artist, title))
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
    else:
        return (None, "Some error happend")
    if result is not None:
        result += "\n\n Lyric source: chartlyrics.com"
    return (result, None)

if __name__ == "__main__":
    print("main")
    art = sys.argv[1]
    mus = sys.argv[2]
    links = fetch_lyric(art, mus)
    print(links)