from lingualyrics.scripts import dbus_handler
from lingualyrics.scripts import lyric


class MainWindowPresenter:
    def __init__(self, window):
        self.window = window

    def start_discovery(self):
        self.dbus_handler = dbus_handler.DbusHandler(self)

    def on_new_music_detected(self, artist, title):
        self.get_lyric(artist, title)

    def get_lyric(self, artist, title):
            print('Now playing', end=": ")
            print('{_artist} - {_title}'.format(_artist=artist, _title=title))
            print('\n')
            print("*" * 20)
            lyric_text = lyric.get_lyric(artist, title)
            if lyric_text is not None:
                # print(lyric_text)
                self.window.set_lyric_text(lyric_text)
            else:
                print("Sorry! no lyric found")

            print("*" * 20)
            print('\n')

    def on_playback_status(self, status):
        self.window.set_play_pause_button_state(status)

    def on_can_seek(self, can_seek):
        self.window.set_seek_slider_sensitivity(can_seek)

    def on_can_go_next(self, can_go_next):
        self.window.set_next_media_button_sensitivity(can_go_next)

    def on_can_go_previous(self, can_go_previous):
        self.window.set_previous_media_button_sensitivity(can_go_previous)

    def on_volume_change(self, vol):
        self.window.set_volume_slider_value(vol)

    def play_pause_button_clicked(self):
        self.dbus_handler.player_play_pause()

    def next_media_button_clicked(self, *args):
        self.dbus_handler.player_next_media()

    def previous_media_button_clicked(self, *args): 
        self.dbus_handler.player_previous_media()

    def volume_button_clicked(self, *args):
        self.dbus_handler.toggle_volume()

    def user_change_volume(self, vol):
        self.dbus_handler.set_player_volume(vol)
