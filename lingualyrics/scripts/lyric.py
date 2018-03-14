import requests
from xml.etree import ElementTree


def get_lyric(artist, title):
    r = requests.get('http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect\
                     ?artist={0}&song={1}'.format(artist, title))
    # print(r.content)
    try:
        tree = ElementTree.fromstring(r.content)
        return tree.find('{http://api.chartlyrics.com/}Lyric').text
    except Exception:
        return None
        # print("XML parse Error", Exception)
