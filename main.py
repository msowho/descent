from gui import DeathQueen
from gi.repository import Gtk


def main():
    win = DeathQueen()
    
    win.connect("destroy", Gtk.main_quit)
    win.show_all()

    Gtk.main()


if __name__ == "__main__":
    main()
