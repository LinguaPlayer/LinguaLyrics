import dbus
import threading
import time
import re
from dbus.mainloop.glib import DBusGMainLoop
DBusGMainLoop(set_as_default=True)


class DbusHandler:

    def __init__(self, presenter):
        self.mpris_player_interface = 'org.mpris.MediaPlayer2.Player'
        self.mpris_player_object_path = '/org/mpris/MediaPlayer2'
        self.properties_changed_signal = 'PropertiesChanged'
        self.freedesktop_propterties_interface = 'org.freedesktop.DBus.Properties'
        self.music_length = 1

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
            self.player = dbus.SessionBus().get_object(self.player_list[0], self.mpris_player_object_path)
            properties = self.player.GetAll(self.mpris_player_interface)
            self.on_properties_change(self.mpris_player_interface, properties)

        bus.add_signal_receiver(self.on_properties_change,
                                dbus_interface=self.freedesktop_propterties_interface,
                                signal_name=self.properties_changed_signal)

    def on_properties_change(self, *args, **kwargs):
        if self.mpris_player_interface != args[0]:
            return
        if 'PlaybackStatus' in args[1]:
            self.on_playback_status(args[1]['PlaybackStatus'])

        if 'CanSeek' in args[1]:
            self.on_can_seek(args[1]['CanSeek'])

        if 'CanGoPrevious' in args[1]:
            self.on_can_go_previous(args[1]['CanGoPrevious'])

        if 'CanGoNext' in args[1]:
            self.on_can_go_next(args[1]['CanGoNext'])
        
        if 'Volume' in args[1]:
            self.on_volume_change(args[1]['Volume'])

        if 'Metadata' in args[1]:
            metadata = args[1]['Metadata']
            self.on_metadata(metadata)

    def on_playback_status(self, status):
        self.presenter.on_playback_status(status)

    def on_can_seek(self, can_seek):
        self.presenter.on_can_seek(can_seek)

    def on_can_go_next(self, can_go_next):
        self.presenter.on_can_go_next(can_go_next)

    def on_can_go_previous(self, can_go_previous):
        self.presenter.on_can_go_previous(can_go_previous)

    def on_player_position_slider_change(self, event):
        while True:
            event.wait()
            position = self.player.GetAll(self.mpris_player_interface)['Position'] 
            self.presenter.on_player_position_change(position, self.music_length)
            time.sleep(1)

    def on_metadata(self, metadata):
        artist = ''
        title = ''
        if 'xesam:artist' in metadata:
            artist = metadata['xesam:artist'][0]
        if 'xesam:title' in metadata:
            title = metadata['xesam:title']
        if 'mpris:length' in metadata:
            self.music_length = metadata['mpris:length']
        if 'mpris:trackid' in metadata:
            self.track_id = metadata['mpris:trackid']

        # Got this signal multiple time
        if (artist, title) != self.last_track:
            self.presenter.on_new_music_detected(artist, title)
            self.last_track = (artist, title)
    
    def player_play_pause(self):
        self.player.PlayPause()
    
    def player_next_media(self):
        self.player.Next()
    
    def player_previous_media(self):
        self.player.Previous() 
    
    def on_volume_change(self, vol):
        self.presenter.on_volume_change(vol)

    def get_volume(self):
        property_interface = dbus.Interface(self.player, dbus_interface=self.freedesktop_propterties_interface)
        return property_interface.Get(self.mpris_player_interface, 'Volume')

    def toggle_volume(self):
        volume = self.get_volume()

        if volume == 0:
            if not hasattr(self, 'volume_before_mute'):
                self.volume_before_mute = 0.5
            self.set_player_volume(self.volume_before_mute)
            
        else:
            self.volume_before_mute = volume
            self.set_player_volume(0)

    def set_player_volume(self, vol):
        property_interface = dbus.Interface(self.player, dbus_interface=self.freedesktop_propterties_interface)
        property_interface.Set('org.mpris.MediaPlayer2.Player', 'Volume', vol)
    
    def set_player_position(self, position):
        iface = dbus.Interface(self.player, self.mpris_player_interface)
        iface.SetPosition(self.track_id, position)



    