#!/usr/bin/env python3
from gi.repository import GLib
import dbus
import lyric
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)

last_track = ('', '')

player = dbus.SessionBus().get_object('org.mpris.MediaPlayer2.clementine',
                                      '/org/mpris/MediaPlayer2')


def on_metadata(*args, **kwargs):

    global last_track

    metadata = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
    artist = ''
    title = ''

    if 'xesam:artist' in metadata:
        artist = metadata['xesam:artist'][0]
    else:
        print("Sorry, Track info has no artist name")
        return
    if 'xesam:title' in metadata:
        title = metadata['xesam:title']
    else:
        print("Sorry, Track info has no title")
        return

    if (artist, title) == last_track:
        return

    # Got this signal multiple time
    last_track = (artist, title)
    get_lyric(artist, title)


def get_lyric(artist, title):
        print('Now playing', end=": ")
        print('{_artist} - {_title}'.format(_artist=artist, _title=title))
        print('\n')
        print("*" * 20)
        lyric_text = lyric.get_lyric(artist, title)
        if lyric_text is not None:
            print(lyric_text)
        else:
            print("Sorry! no lyric found")

        print("*" * 20)
        print('\n')


player.connect_to_signal("PropertiesChanged", on_metadata)
metadata = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
on_metadata()

# wait for events
main = GLib.MainLoop()
main.run()
