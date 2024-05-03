import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class MyWindow(Gtk.Window):

    def __init__(self):
        super().__init__(title="Hello World")
        self.button_box = Gtk.Box(spacing=6)
        self.btn_start = Gtk.Button(label="Click Here")
        self.btn_start.connect("clicked", self.on_button_clicked)
        self.button_box(self.button)

    def on_start_button_clicked(self, widget):
        print("Hello World")


def main()->None:
    win = MyWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()


if __name__=="__main__":
    main()