import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib 
from lingualyrics.gui.mainwindow import mainwindow_presenter
from lingualyrics.scripts import utils


class Handler:
    def __init__(self, presenter, window):
        self.presenter = presenter
        self.window = window

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
    
    def on_refresh_button_clicked(self, *args):
        self.presenter.refresh_player_list()
    
    def on_player_selected(self, *args):
        active_text = args[0].get_active_text()
        if active_text is not None:
            self.presenter.on_player_selected(active_text)
    
    def on_font_plus_button_clicked(self, *args):
        self.presenter.font_plus_button_clicked(self.window.get_font_size())

    def on_font_minus_button_clicked(self, *args):
        self.presenter.font_minus_button_clicked(self.window.get_font_size())
    
    def on_color_picker_button_clicked(self, *args):
        # dlg = Gtk.ColorSelectionDialog("Select color")
        # help(Gtk.ColorSelectionDialog)
        # response = dlg.run()
        # print(response)
        print("TO DO")


class MainWindow():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("lingualyrics/gui/mainwindow/lingua_lyric.glade")
        self.presenter = mainwindow_presenter.MainWindowPresenter(self)

        self.window = builder.get_object("window_main")
        self.window.show_all()
        self.lyric_text_view = builder.get_object("lyric_text_view")
        self.lyric_text_buffer = builder.get_object("lyric_text_buffer")
        self.size_tag = self.lyric_text_buffer.create_tag("font-size")
        self.set_font_size(14)
        # self.color_tag = self.lyric.lyric_text_buffer.create_tag("foreground-color")

        self.next_media_button = builder.get_object("next_media_button")
        self.play_pause_button = builder.get_object("play_pause_button")
        self.previouse_media_button = builder.get_object("previouse_media_button")
        self.play_icon = builder.get_object("play_icon")
        self.pause_icon = builder.get_object("pause_icon")
        self.player_position_slider = builder.get_object("player_position_slider")
        self.player_position_adjustment = builder.get_object("player_position_adjustment")
        self.player_position_label = builder.get_object("player_position_label")
        self.volume_adjustment = builder.get_object("player_volume_adjustment")
        self.volume_slider = builder.get_object("player_volume_slider")
        self.volume_button = builder.get_object("volume_button")
        self.player_list_combobox = builder.get_object("player_list_comboboxtext")

        self.player_list = []
        self.presenter.start_discovery()
        builder.connect_signals(Handler(self.presenter, self))
        Gtk.main()

    def update_window_title(self, title):
        self.window.set_title(title + " - " + "LinguaLyrics")

    def set_font_size(self, value):
        self.size_tag.set_property('size_points', value)

    def get_font_size(self):
        size = self.size_tag.get_property('size_points')
        return size

    def set_lyric_style(self):
        start = self.lyric_text_buffer.get_start_iter()
        end = self.lyric_text_buffer.get_end_iter()
        self.lyric_text_buffer.apply_tag(self.size_tag, start, end)

    def set_lyric_text(self, text):
        self.lyric_text_view.get_buffer().set_text(text)
        self.set_lyric_style()
    
    def set_next_media_button_sensitivity(self, sensitive):
        self.next_media_button.set_sensitive(sensitive)
        
    def set_previous_media_button_sensitivity(self, sensitive): 
        self.previouse_media_button.set_sensitive(sensitive)

    def set_play_pause_button_sensitivity(self, sensitive):
        self.play_pause_button.set_sensitive(sensitive)

    def set_play_pause_button_state(self, state):
        if state == "Playing":
            self.play_pause_button.set_image(self.pause_icon)
        if state == "Paused":
            self.play_pause_button.set_image(self.play_icon)

    def set_seek_slider_sensitivity(self, sensitive): 
        self.player_position_slider.set_sensitive(sensitive)

    def set_volume_slider_value(self, vol):
        self.volume_adjustment.set_value(vol * 20)
    
    def set_volume_sensitivity(self, sensitive):
        self.volume_slider.set_sensitive(sensitive)
        self.volume_button.set_sensitive(sensitive)

    def set_player_slider_value(self, position, length):
        self.player_position_label.set_text(utils.convert_microsecond_to_player_time(position))
        self.player_position_adjustment.set_upper(length)
        self.player_position_adjustment.set_value(position)
    
    def set_player_list_combobox(self, player_list):
        previous_player = self.player_list_combobox.get_active_text()
        for i in self.player_list:
            self.player_list_combobox.remove(0)
        self.player_list = player_list

        player_list_names = []
        for player_name in player_list:
            player_name = player_name.split('.')[-1]
            self.player_list_combobox.append_text(player_name)
            player_list_names.append(player_name)

        if previous_player in player_list_names: 
            index = player_list_names.index(previous_player)
            self.set_active_player_index(index)
        else:
            self.set_active_player_index(-1)

    def player_buttons_sensitivity(self, sensitive):
        self.set_next_media_button_sensitivity(sensitive)
        self.set_previous_media_button_sensitivity(sensitive)
        self.set_seek_slider_sensitivity(sensitive)
        self.set_volume_sensitivity(sensitive)
        self.set_seek_slider_sensitivity(sensitive)
        self.set_play_pause_button_sensitivity(sensitive)
    
    def set_active_player_index(self, index):
        self.player_list_combobox.set_active(index)
