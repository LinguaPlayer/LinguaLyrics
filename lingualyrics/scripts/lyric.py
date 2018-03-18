import requests
from xml.etree import ElementTree


def get_lyric(artist, title, callback):
    r = requests.get('http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect\
                     ?artist={0}&song={1}'.format(artist, title))
    try:
        tree = ElementTree.fromstring(r.content)
        result = tree.find('{http://api.chartlyrics.com/}Lyric').text
        callback(artist, title, result)

    except Exception as e:
        print(e)
        callback(artist, title, None)
