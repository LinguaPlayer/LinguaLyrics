import requests
from lingualyrics.scripts.lyricsources import chartlyrics
from lingualyrics.scripts.lyricsources import lingualyrics_server 


def get_lyric(artist, title, tried_with_fingerprint, callback):
    (result, error) = lingualyrics_server.get_lyric(artist, title)
    
    callback(artist, title, result, tried_with_fingerprint, error)
