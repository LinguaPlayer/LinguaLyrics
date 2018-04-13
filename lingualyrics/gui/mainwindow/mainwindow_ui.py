import gi
import os
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib,Gdk
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

    def on_leave_window(self, *args):
        # self.window.hide_menus_and_title_bar()
        # print("on leave window")
        # print(args)
        pass

    def on_enter_window(self, *args):
        # self.window.show_menus_and_title_bar()
        # print("on enter window")
        # print(args)
        pass


class MainWindow():

    def __init__(self):
        builder = Gtk.Builder()
        base_path = os.path.abspath(os.path.dirname(__file__))
        ui_layout_file = os.path.join(base_path, "main_window.glade")
        builder.add_from_file(ui_layout_file)
        self.presenter = mainwindow_presenter.MainWindowPresenter(self)

        self.window = builder.get_object("window_main")
        self.window.show_all()
        self.lyric_text_view = builder.get_object("lyric_text_view")
        self.lyric_text_buffer = builder.get_object("lyric_text_buffer")
        self.size_tag = self.lyric_text_buffer.create_tag("font-size")
        self.try_again_tag = self.lyric_text_buffer.create_tag("clickable_tag")
        self.try_again_tag.connect("event", self.handle_try_again_click)
        self.try_again_tag.set_property("underline", True)

        self.blue_tag_color = self.lyric_text_buffer.create_tag("clickable_color")
        self.blue_tag_color.set_property("foreground", "blue")

        self.try_again_with_fingerprint_tag = self.lyric_text_buffer.create_tag("try_again_with_fingerprint")
        self.try_again_with_fingerprint_tag.set_property("underline", True)
        self.try_again_with_fingerprint_tag.connect("event", self.handle_try_again_with_fingerprint_click)

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

    def show_message(self, message):
        self.lyric_text_view.get_buffer().set_text(message)
        self.set_lyric_style()

    def lyric_found_successfully(self, lyric_text, tried_with_fingerprint):
        if not tried_with_fingerprint:
            lyric_is_wrong = "\n\nLyric is wrong?"
            retry_message = " Try with audio fingerprint"
            lyric_text += lyric_is_wrong + retry_message
            self.show_message(lyric_text)
            start = self.lyric_text_buffer.get_iter_at_offset(len(lyric_text)-len(retry_message))
            end = self.lyric_text_buffer.get_iter_at_offset(len(lyric_text))
            self.lyric_text_buffer.apply_tag(self.try_again_with_fingerprint_tag, start, end)
            self.lyric_text_buffer.apply_tag(self.blue_tag_color, start, end)
        else:
            self.show_message(lyric_text)

    def lyric_not_found(self, message, tried_with_fingerprint):
        if not tried_with_fingerprint:
            retry_message = "\nTry with audio fingerprint"
            message += retry_message
            self.lyric_text_view.get_buffer().set_text(message)
            start = self.lyric_text_buffer.get_iter_at_offset(len(message)-len(retry_message))
            end = self.lyric_text_buffer.get_iter_at_offset(len(message))
            self.lyric_text_buffer.apply_tag(self.try_again_with_fingerprint_tag, start, end)
            self.lyric_text_buffer.apply_tag(self.blue_tag_color, start, end)
        else:
            self.lyric_text_view.get_buffer().set_text(message)
        self.set_lyric_style()

    def show_error_with_retry_button(self, message):
        retry_message = "\nTry again"
        message += retry_message
        self.lyric_text_view.get_buffer().set_text(message)
        start = self.lyric_text_buffer.get_iter_at_offset(len(message)-len(retry_message))
        end = self.lyric_text_buffer.get_iter_at_offset(len(message))
        self.set_lyric_style()
        self.lyric_text_buffer.apply_tag(self.try_again_tag, start, end)
        self.lyric_text_buffer.apply_tag(self.blue_tag_color, start, end)

    def handle_try_again_click(self, *args):    
        if args[2].type == Gdk.EventType.BUTTON_RELEASE:
            print("Retry")
            self.presenter.retry_fetching_lyrics()

    def handle_try_again_with_fingerprint_click(self, *args):    
        if args[2].type == Gdk.EventType.BUTTON_RELEASE:
            print("Retry with fingerprint")
            self.presenter.get_lyric_with_audiofingerprint()

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

    # def hide_menus_and_title_bar(self):
    #     self.window.set_decorated(False)

    # def show_menus_and_title_bar(self):
    #     self.window.set_decorated(True)
