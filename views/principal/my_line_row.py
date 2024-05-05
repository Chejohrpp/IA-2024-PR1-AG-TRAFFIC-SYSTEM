
from gi.repository import GObject, Gtk

from views.model_construction.items import MyLine

class MyLineRow(GObject.Object):

    def __init__(self, my_line: MyLine):
        super().__init__()
        self.my_line = my_line
        self.name = my_line.name
        self.percent = my_line.estimated_percentage