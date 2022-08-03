from fco import FCO
import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DeathQueen(Gtk.Window):
    def __init__(self):
        super().__init__(title="Death Queen")
        
        self.set_default_size(800, 500)

        self.grid = Gtk.Grid()
        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)
        self.add(self.grid)

        self.current_fco = FCO.create_empty()

        self.update_lists()

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

        self.grid.attach(self.scrollable_treelist, 1, Gtk.PositionType.LEFT, 1, 1)
        self.grid.attach(self.scrollable_message_treelist, 2, Gtk.PositionType.LEFT, 1, 1)
        
        self.scrollable_treelist.add(self.treeview)
        self.scrollable_message_treelist.add(self.message_treeview)
    
    def update_lists(self):
        self.group_liststore = Gtk.ListStore(str)
        for group in self.current_fco.groups:
            name = group["name"]
            self.group_liststore.append([name])
        
        self.message_liststore = Gtk.ListStore(str)
        if len(self.current_fco.groups) > 0 and len(group["messages"]) != 0:
            for message in self.current_fco.groups[0]["messages"]:
                name = message["name"]
                self.message_liststore.append([name])
