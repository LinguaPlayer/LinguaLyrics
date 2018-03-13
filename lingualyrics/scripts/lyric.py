import requests
from xml.etree import ElementTree

def get_lyric(artis, title):
    r = requests.get('http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={0}&song={1}'.format(artis,title))
    tree = ElementTree.fromstring(r.content)
    return tree.find('{http://api.chartlyrics.com/}Lyric').text