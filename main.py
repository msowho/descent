from gui import DeathQueen
from gi.repository import Gtk


def main():
    death_queen = DeathQueen()

    death_queen.connect("destroy", Gtk.main_quit)
    death_queen.show_all()

    Gtk.main()


if __name__ == "__main__":
    main()
