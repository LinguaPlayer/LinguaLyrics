import dbus
import re
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)


class DbusHandler:
    def __init__(self, presenter):
        self.presenter = presenter
        self.last_track = ('', '')
        bus = dbus.SessionBus()
        # Get list of players
        self.player_list = []
        for service in bus.list_names():
            if re.match('org.mpris.MediaPlayer2.', service):
                self.player_list.append(service)

        # Get the metadat of current track of first item playerList
        if self.player_list != []:
            player = dbus.SessionBus().get_object(self.player_list[0], '/org/mpris/MediaPlayer2')
            metadata = player.Get('org.mpris.MediaPlayer2.Player', 'Metadata')
            self.on_metadata(metadata)

        bus.add_signal_receiver(self.on_properties_change,
                                dbus_interface='org.freedesktop.DBus.Properties',
                                signal_name='PropertiesChanged')

    def on_properties_change(self, *args, **kwargs):
        if 'Metadata' in args[1]:
            metadata = args[1]['Metadata']
            self.on_metadata(metadata)

    def on_metadata(self, metadata):
        artist = ''
        title = ''
        if 'xesam:artist' in metadata:
            artist = metadata['xesam:artist'][0]
        if 'xesam:title' in metadata:
            title = metadata['xesam:title']

        # Got this signal multiple time
        if (artist, title) != self.last_track:
            self.presenter.on_new_music_detected(artist, title)
            self.last_track = (artist, title)
