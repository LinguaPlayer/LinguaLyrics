import threading
from lingualyrics.scripts import dbus_handler
from lingualyrics.scripts import aidmatch
from lingualyrics.scripts import lyric
from gi.repository import GLib


class MainWindowPresenter:
    def __init__(self, window):
        self.window = window
        self.thread_event = threading.Event()
        self.music_data = None
        self.fetched_lyric_data = None
        self.retried = False
        self.music_path = None

    def start_discovery(self):
        self.dbus_handler = dbus_handler.DbusHandler(self)

        player_list = self.dbus_handler.get_available_players()
        if player_list != []:
            self.on_player_selected(player_list[0].split('.')[-1])
            self.window.set_active_player_index(0)

        thread = threading.Thread(target=self.dbus_handler.on_player_position_slider_change, args=(self.thread_event, ))
        thread.daemon = True
        thread.start()

    def on_player_selected(self, player_name):
        if self.dbus_handler.is_player_available(player_name):
            self.dbus_handler.create_player_proxy(player_name)
            self.player_found()
        else:
            self.player_closed()
            self.dbus_handler.get_available_players()

    def on_new_music_detected(self, artist, title, path):
        self.retried = False
        self.window.update_window_title(artist, title)
        self.music_path = path
        if path.startswith("file://"):
            self.music_path = self.music_path[7:]
        enable_retry_with_fingerprint = True
        # self.music_path is None or empty
        if not self.music_path:
            enable_retry_with_fingerprint = False
        self.get_lyric(artist, title, enable_retry_with_fingerprint)
    
    def retry_fetching_lyrics(self):
        self.retried = True
        self.get_lyric(self.music_data[0], self.music_data[1], True)
    
    def get_lyric_with_audiofingerprint(self):
        self.show_message("Getting the metadata using fingerprint ... ")
        thread = threading.Thread(target=aidmatch.aidmatch, args=(self.music_path, self.on_download_metadata))
        thread.daemon = True
        thread.start()
    
    def on_download_metadata(self, results):
        try:
            score, rid, title, artist = next(results)
            self.window.update_window_title(artist, title)
            self.retried = True
            GLib.idle_add(self.get_lyric, artist, title, False)
        except StopIteration:
            print("No metadata found for this fingerprint")
            GLib.idle_add(self.show_lyric_not_found, "Sorry we couldn't find music metadata using fingerprint", False)

    def on_lyric_fetch(self, artist, title, lyric_text, add_try_with_fingerprint, error):
        if (artist, title) != self.music_data:
            return

        if self.fetched_lyric_data == self.music_data and not self.retried:
            print("This really happens!!!!!")
            return

        self.retried = False

        self.fetched_lyric_data = (artist, title)

        if error is None:
            if lyric_text is not None:
                GLib.idle_add(self.show_lyric_found, lyric_text, add_try_with_fingerprint)
            else:
                GLib.idle_add(self.show_lyric_not_found, "Sorry! no lyric found for this music", add_try_with_fingerprint)
        else:
                GLib.idle_add(self.show_error, error)

    def get_lyric(self, artist, title, add_try_with_fingerprint):
            self.show_message('Searching lyric for {_artist} - {_title}'.format(_artist=artist, _title=title))
            self.music_data = (artist, title)
            thread = threading.Thread(target=lyric.get_lyric, args=(artist, title, add_try_with_fingerprint, self.on_lyric_fetch))
            thread.daemon = True
            thread.start()

    def show_message(self, message):
        self.window.show_message(message)

    def show_lyric_found(self, message, add_try_with_fingerprint):
        self.window.lyric_found_successfully(message, add_try_with_fingerprint)
    
    def show_lyric_not_found(self, message, add_try_with_fingerprint):
        self.window.lyric_not_found(message, add_try_with_fingerprint)
    
    def show_error(self, message):
        self.window.show_error_with_retry_button(message)

    def on_playback_status(self, status):
        if status == "Playing":
            self.thread_event.set()
        else:
            self.thread_event.clear()
        self.window.set_play_pause_button_state(status)

    def on_can_seek(self, can_seek):
        self.window.set_seek_slider_sensitivity(can_seek)

    def on_can_go_next(self, can_go_next):
        self.window.set_next_media_button_sensitivity(can_go_next)

    def on_can_go_previous(self, can_go_previous):
        self.window.set_previous_media_button_sensitivity(can_go_previous)

    def on_volume_change(self, vol):
        self.window.set_volume_slider_value(vol)

    def on_player_position_change(self, position, length):
        self.window.set_player_slider_value(position, length)

    def play_pause_button_clicked(self):
        self.dbus_handler.player_play_pause()

    def next_media_button_clicked(self, *args):
        self.dbus_handler.player_next_media()
    
    def font_plus_button_clicked(self, current_size):
        print(current_size)
        if current_size < 30:
            self.window.set_font_size(current_size+0.5)
            self.window.set_lyric_style()

    def font_minus_button_clicked(self, current_size):
        if current_size > 10:
            self.window.set_font_size(current_size-0.5)
            self.window.set_lyric_style()

    def previous_media_button_clicked(self, *args): 
        self.dbus_handler.player_previous_media()

    def volume_button_clicked(self, *args):
        self.dbus_handler.toggle_volume()

    def user_change_volume(self, vol):
        self.dbus_handler.set_player_volume(vol)
    
    def user_change_player_position(self, position):
        self.thread_event.clear()
        self.dbus_handler.set_player_position(position)
        self.thread_event.set()
    
    def set_player_list_comboboxtext(self, player_list):
        if player_list == []:
            self.player_closed()
        self.window.set_player_list_combobox(player_list)
    
    def refresh_player_list(self):
        player_list = self.dbus_handler.get_available_players()
        self.set_player_list_comboboxtext(player_list)
    
    def player_closed(self):
        self.window.player_buttons_sensitivity(False)
        self.window.set_active_player_index(-1)
    
    def player_found(self):
        self.window.player_buttons_sensitivity(True)
