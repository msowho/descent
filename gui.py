from fco import FCO
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DeathQueen(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Death Queen")

        self.set_resizable(False)

        self.grid = Gtk.Grid()
        
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.add(self.grid)

        self.current_fco = FCO.create_empty()

        self.update_lists()

        self.create_toolbar()
        self.create_treelist()

    def create_toolbar(self) -> None:
        self.toolbar = Gtk.Toolbar()
        self.grid.attach(self.toolbar, 0, 0, 9, 1)

        self.button_new = Gtk.ToolButton()
        self.button_new.set_icon_name("document-new")
        self.toolbar.insert(self.button_new, 0)

        self.button_open = Gtk.ToolButton()
        self.button_open.set_icon_name("document-open")
        self.toolbar.insert(self.button_open, 1)

        self.button_new.connect("clicked", self.on_button_new_clicked)
        self.button_open.connect("clicked", self.on_button_open_clicked)

    def create_treelist(self) -> None:
        self.group_treeview = Gtk.TreeView(model=self.group_liststore)
        self.message_treeview = Gtk.TreeView(model=self.message_liststore)

        self.content_container = Gtk.Box()
        self.grid.attach(self.content_container, 0, 1, 9, 9)

        self.content_grid = Gtk.Grid()

        self.content_grid.set_column_homogeneous(True)
        self.content_grid.set_row_homogeneous(True)

        self.content_container.set_center_widget(self.content_grid)

        self.group_renderer = Gtk.CellRendererText()
        self.group_column = Gtk.TreeViewColumn("Groups", self.group_renderer, text=0)
        self.group_treeview.append_column(self.group_column)

        self.message_renderer = Gtk.CellRendererText()
        self.message_column = Gtk.TreeViewColumn("Messages", self.message_renderer, text=0)
        self.message_treeview.append_column(self.message_column)

        self.group_scrollable = Gtk.ScrolledWindow()
        self.group_scrollable.set_vexpand(True)
        self.group_scrollable.set_min_content_width(200)

        self.message_scrollable = Gtk.ScrolledWindow()
        self.message_scrollable.set_vexpand(True)

        self.content_grid.attach(self.group_scrollable, 0, 0, 1, 1)
        self.content_grid.attach_next_to(self.message_scrollable, self.group_scrollable, 0, 1, 1)

        self.group_scrollable.add(self.group_treeview)
        self.message_scrollable.add(self.message_treeview)

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

    def on_button_new_clicked(self, element) -> None:
        pass

    def on_button_open_clicked(self, element) -> None:
        pass
