import requests
from lingualyrics.scripts.lyricsources import chartlyrics


def get_lyric(artist, title, tried_with_fingerprint, callback):
    (result, error) = chartlyrics.get_lyric(artist, title)
    callback(artist, title, result, tried_with_fingerprint, error)
