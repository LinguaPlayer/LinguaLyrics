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
        # else:
        #     print("Sorry, Track info has no artist name")
        #     return

        # else:
        #     print("Sorry, Track info has no title")
        #     return

