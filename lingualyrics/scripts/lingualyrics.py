#!/usr/bin/env python3
from gi.repository import Playerctl, GLib
import lyric

player = Playerctl.Player(player_name='clementine')

last_track = ('','')

def on_metadata(player, e):
    global last_track
    if 'xesam:artist' in e.keys() and 'xesam:title' in e.keys():
        artist = e['xesam:artist'][0]
        title = e['xesam:title']
        #Got this signal multiple time
        if (artist, title) == last_track:
            return

        print('Now playing', end=": ")
        print('{_artist} - {_title}'.format(_artist= artist, _title=title))
        print('\n')
        print("*" * 20)
        lyric_text = lyric.get_lyric(artist, title)
        if lyric_text is not None:
            print(lyric_text)
        else:
            print("Sorry! no lyric found") 

        last_track = (artist,title)
        print("*" * 20)
        print('\n')

player.on('metadata', on_metadata)

# wait for events
main = GLib.MainLoop()
main.run()