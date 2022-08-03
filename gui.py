from fco import FCO
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DeathQueen(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Death Queen")

        self.set_default_size(800, 500)

        self.grid = Gtk.Grid()
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.current_fco = FCO.create_empty()

        self.update_lists()

        self.create_toolbar()
        self.create_treelist()

    def create_toolbar(self) -> None:
        self.toolbar = Gtk.Toolbar()
        self.grid.attach(self.toolbar, 0, 0, 1, 1)

        self.button_new = Gtk.ToolButton()
        self.button_new.set_icon_name("document-new")
        self.toolbar.insert(self.button_new, 0)

        self.button_open = Gtk.ToolButton()
        self.button_open.set_icon_name("document-open")
        self.toolbar.insert(self.button_open, 1)

        #button_bold.connect("clicked", self.on_button_clicked, self.tag_bold)
        #button_italic.connect("clicked", self.on_button_clicked, self.tag_italic)
        #button_underline.connect("clicked", self.on_button_clicked, self.tag_underline)

    def create_treelist(self) -> None:
        self.treeview = Gtk.TreeView(model=self.group_liststore)
        self.message_treeview = Gtk.TreeView(model=self.message_liststore)

        renderer = Gtk.CellRendererText()

        column = Gtk.TreeViewColumn("Groups", renderer, text=0)
        self.treeview.append_column(column)

        column = Gtk.TreeViewColumn("Messages", renderer, text=0)
        self.message_treeview.append_column(column)

        self.scrollable_treelist = Gtk.ScrolledWindow()
        self.scrollable_treelist.set_vexpand(True)

        self.scrollable_message_treelist = Gtk.ScrolledWindow()
        self.scrollable_message_treelist.set_vexpand(True)

        self.content_grid = Gtk.Grid()
        self.content_grid.set_column_homogeneous(True)
        self.content_grid.set_row_homogeneous(True)
        self.grid.attach(self.content_grid, 0, 1, 1, 1)

        self.content_grid.attach(self.scrollable_treelist, 0,
                                   Gtk.PositionType.LEFT, 1, 1)
        self.content_grid.attach(self.scrollable_message_treelist,
                                   0, Gtk.PositionType.LEFT, 1, 1)

        self.scrollable_treelist.add(self.treeview)
        self.scrollable_message_treelist.add(self.message_treeview)

    def update_lists(self) -> None:
        self.group_liststore = Gtk.ListStore(str)
        for group in self.current_fco.groups:
            name = group["name"]
            self.group_liststore.append([name])

        self.message_liststore = Gtk.ListStore(str)
        if len(self.current_fco.groups) > 0 and len(group["messages"]) != 0:
            for message in self.current_fco.groups[0]["messages"]:
                name = message["name"]
                self.message_liststore.append([name])
