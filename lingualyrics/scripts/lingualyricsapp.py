import sys
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gio
from gi.repository import Gtk

from lingualyrics.gui.mainwindow import mainwindow_ui
from lingualyrics.scripts import dbus_handler


class App(Gtk.Application):

    def __init__(self):
        Gtk.Application.__init__(self,
                                 application_id="org.gnome.example",
                                 flags=Gio.ApplicationFlags.FLAGS_NONE)

    def do_activate(self):
        self.main_window = mainwindow_ui.MainWindow()


def main():
    app = App()
    app.run(sys.argv)
