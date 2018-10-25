import requests
from lingualyrics.scripts.lyricsources import chartlyrics
from lingualyrics.scripts.lyricsources import vagalume

def get_lyric(artist, title, tried_with_fingerprint, callback):
    (result, error) = vagalume.get_lyric(artist, title)
    callback(artist, title, result, tried_with_fingerprint, error)