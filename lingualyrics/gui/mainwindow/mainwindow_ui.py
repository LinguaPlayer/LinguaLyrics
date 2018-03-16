import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from lingualyrics.gui.mainwindow import mainwindow_presenter


class Handler:
    def on_window_main_destroy(self, *args):
        Gtk.main_quit(*args)

    def onButtonPressed(self, button):
        print("Hello World!")


class MainWindow():

    def __init__(self):
        builder = Gtk.Builder()
        builder.add_from_file("lingualyrics/gui/mainwindow/lingua_lyric.glade")
        builder.connect_signals(Handler())

        self.window = builder.get_object("window_main")
        self.window.show_all()
        self.presenter = mainwindow_presenter.MainWindowPresenter(self)
        self.lyric_text_view = builder.get_object("lyric_text_view")
        self.presenter.start_discovery()
        Gtk.main()
   
    def set_lyric_text(self, text):
        self.lyric_text_view.get_buffer().set_text(text)
    