from fco import FCO
from hh_table import HHTable

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class DeathQueen(Gtk.Window):
    def __init__(self) -> None:
        super().__init__(title="Descent")

        self.set_resizable(False)

        self.grid = Gtk.Grid()

        self.grid.set_column_homogeneous(True)
        self.grid.set_row_homogeneous(True)

        self.add(self.grid)

        self.current_fco = FCO.create_empty()
        self.fco_filepath = None

        self.current_group_index = 0

        self.current_hh_name = "Common"
        self.current_hh_table = HHTable(self.current_hh_name)

        self.group_liststore = Gtk.ListStore(str)
        self.message_liststore = Gtk.ListStore(str, str)

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
        self.group_column = Gtk.TreeViewColumn(
            "Groups", self.group_renderer, text=0)
        self.group_treeview.append_column(self.group_column)

        self.message_renderer = Gtk.CellRendererText()

        self.message_renderer_editable = Gtk.CellRendererText()
        
        self.message_renderer_editable.set_property("editable", True)
        self.message_renderer_editable.connect("edited", self.on_message_edited)

        self.message_column = Gtk.TreeViewColumn(
            "Name", self.message_renderer, text=0)
        self.message_column_editable = Gtk.TreeViewColumn(
            "String", self.message_renderer_editable, text=1)

        self.message_treeview.append_column(self.message_column)
        self.message_treeview.append_column(self.message_column_editable)

        self.group_scrollable = Gtk.ScrolledWindow()
        self.group_scrollable.set_vexpand(True)
        self.group_scrollable.set_min_content_width(300)

        self.message_scrollable = Gtk.ScrolledWindow()
        self.message_scrollable.set_vexpand(True)

        self.content_grid.attach(self.message_scrollable, 0, 0, 1, 1)
        self.content_grid.attach_next_to(
            self.group_scrollable, self.message_scrollable, 0, 1, 1)

        self.group_scrollable.add(self.group_treeview)
        self.message_scrollable.add(self.message_treeview)

        self.group_selection = self.group_treeview.get_selection()
        self.group_selection.connect("changed", self.on_treeview_selected)

        self.current_treeiter = self.group_selection.get_selected()[1]

    def update_lists(self, update_group=True) -> None:
        if update_group:
            self.group_liststore.clear()
            for group in self.current_fco.groups:
                name = group["name"]
                self.group_liststore.append([name])

        self.message_liststore.clear()
        group = self.current_fco.groups[self.current_group_index]
        
        if len(self.current_fco.groups) > 0 and len(group["messages"]) != 0:
            for message in group["messages"]:
                name = message["name"]
                string = self.current_hh_table.convert_symbols_to_string(message["symbols"])

                self.message_liststore.append([name, string])
        
        self.group_treeview.set_model(self.group_liststore)
        self.message_treeview.set_model(self.message_liststore)

    def on_button_new_clicked(self, element) -> None:
        if element != self.button_new:
            return

        self.current_fco = FCO.create_empty()
        self.fco_filepath = None

        self.update_lists()

    def on_button_open_clicked(self, element) -> None:
        if element != self.button_open:
            return

        dialog = Gtk.FileChooserDialog(
            title="Please choose a file", parent=self, action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL,
            Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN,
            Gtk.ResponseType.OK,
        )

        self.add_filters(dialog)

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            self.load_fco(dialog)

        dialog.destroy()
    
    def on_treeview_selected(self, selection) -> None:
        model, treeiter = selection.get_selected()
        if treeiter != None and treeiter != self.current_treeiter:
            self.current_group_index = self.get_group_index(model, treeiter)
            self.current_treeiter = treeiter
            
            self.update_lists(False)

    def on_message_edited(self, element, row, new_value):
        name = self.message_liststore[row][0]
        message_index = self.get_message_index(name)

        group = self.current_fco.groups[self.current_group_index]
        message = group["messages"][message_index]

        message["symbols"] = self.current_hh_table.convert_string_to_symbols(new_value)

        self.update_lists(False)

    def get_group_index(self, model, treeiter) -> int:
        group_name = model[treeiter][0]
        for i, group in enumerate(self.current_fco.groups):
            if group["name"] == group_name:
                return i
        return 0

    def get_message_index(self, name) -> int:
        group = self.current_fco.groups[self.current_group_index]
        for i, message in enumerate(group["messages"]):
            if message["name"] == name:
                return i
        return 0
        
    def add_filters(self, dialog: Gtk.FileChooserDialog) -> None:
        filter = Gtk.FileFilter()

        filter.set_name("Unleashed text format")
        filter.add_pattern("*.fco")

        dialog.add_filter(filter)
    
    def load_fco(self, dialog) -> None:
        self.fco_filepath = dialog.get_filename()
        self.current_group_index = 0

        with open(self.fco_filepath, 'rb') as f:
            self.current_fco = FCO(f)
            self.current_fco.read_fco(0)

            self.update_lists()
