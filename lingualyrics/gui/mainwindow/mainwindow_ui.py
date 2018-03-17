import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from lingualyrics.gui.mainwindow import mainwindow_presenter
from lingualyrics.scripts import utils

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
    
    def on_volume_button_clicked(self, *args):
        self.presenter.volume_button_clicked()
    
    def on_volum_slider_value_changed(self, *args):
        self.presenter.user_change_volume(args[0].get_value()/20)
    
    def on_position_slider_click(self, *args):
        # self.presenter.user_change_player_position(args[0].get_value())
        pass


class MainWindow():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("lingualyrics/gui/mainwindow/lingua_lyric.glade")
        self.presenter = mainwindow_presenter.MainWindowPresenter(self)

        self.window = builder.get_object("window_main")
        self.window.show_all()
        self.lyric_text_view = builder.get_object("lyric_text_view")

        self.next_media_button = builder.get_object("next_media_button")
        self.play_pause_button = builder.get_object("play_pause_button")
        self.previouse_media_button = builder.get_object("previouse_media_button")
        self.play_icon = builder.get_object("play_icon")
        self.pause_icon = builder.get_object("pause_icon")
        self.player_position_slider = builder.get_object("player_position_slider")
        self.player_position_adjustment = builder.get_object("player_position_adjustment")
        self.player_position_label = builder.get_object("player_position_label")
        self.volume_slider = builder.get_object("player_volume_adjustment")

        self.presenter.start_discovery()
        builder.connect_signals(Handler(self.presenter))
        Gtk.main()
   
    def set_lyric_text(self, text):
        self.lyric_text_view.get_buffer().set_text(text)
    
    def set_next_media_button_sensitivity(self, sensitive):
        self.next_media_button.set_sensitive(sensitive)
        
    def set_previous_media_button_sensitivity(self, sensitive): 
        self.previouse_media_button.set_sensitive(sensitive)
    
    def set_play_pause_button_state(self, state):
        if state == "Playing":
            self.play_pause_button.set_image(self.pause_icon)
        if state == "Paused":
            self.play_pause_button.set_image(self.play_icon)

    def set_seek_slider_sensitivity(self, sensitive): 
        self.player_position_slider.set_sensitive(sensitive)

    def set_volume_slider_value(self, vol):
        self.volume_slider.set_value(vol * 20)

    def set_player_slider_value(self, position, length):
        self.player_position_label.set_text(utils.convert_microsecond_to_player_time(position))
        self.player_position_adjustment.set_upper(length)
        self.player_position_adjustment.set_value(position)