import requests
from lingualyrics.scripts.lyricsources import chartlyrics


def get_lyric(artist, title, callback):
    (result, error) = chartlyrics.get_lyric(artist, title)
    callback(artist, title, result, error)
