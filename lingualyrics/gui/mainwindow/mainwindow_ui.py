import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from lingualyrics.gui.mainwindow import mainwindow_presenter


class Handler:
    def __init__(self, presenter):
        self.presenter = presenter

    def on_window_main_destroy(self, *args):
        Gtk.main_quit(*args)

    def on_play_pause_button_clicked(self, *args):
        self.presenter.play_pause_button_clicked()

    def on_next_media_button_clicked(self, *args):
        self.presenter.next_media_button_clicked()
        
    def on_previous_media_button_clicked(self, *args): 
        self.presenter.previous_media_button_clicked()


class MainWindow():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("lingualyrics/gui/mainwindow/lingua_lyric.glade")
        self.presenter = mainwindow_presenter.MainWindowPresenter(self)
        builder.connect_signals(Handler(self.presenter))

        self.window = builder.get_object("window_main")
        self.window.show_all()
        self.lyric_text_view = builder.get_object("lyric_text_view")

        self.next_media_button = builder.get_object("next_media_button")
        self.play_pause_button = builder.get_object("play_pause_button")
        self.previouse_media_button = builder.get_object("previouse_media_button")
        self.play_icon = builder.get_object("play_icon")
        self.pause_icon = builder.get_object("pause_icon")
        self.player_position_slider = builder.get_object("player_position_slider")

        self.presenter.start_discovery()
        Gtk.main()
   
    def set_lyric_text(self, text):
        self.lyric_text_view.get_buffer().set_text(text)
    
    def set_next_media_button_sensitivity(self, sensitive):
        self.next_media_button.set_sensitive(sensitive)
        
    def set_previous_media_button_sensitivity(self, sensitive): 
        self.previouse_media_button.set_sensitive(sensitive)
    
    def set_play_pause_button_state(self, state):
        if state == "Playing":
            self.play_pause_button.set_image(self.play_icon)
        if state == "Paused":
            self.play_pause_button.set_image(self.pause_icon)

    def set_seek_slider_sensitivity(self, sensitive): 
        self.player_position_slider.set_sensitive(sensitive)
    
