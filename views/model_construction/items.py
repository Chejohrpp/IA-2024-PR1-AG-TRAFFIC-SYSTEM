"""Simple example items.

These items are used in various tests.
"""
from math import pi
import math
import gi
import uuid
import base64

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk

from gaphas.connector import Handle
from gaphas.item import NW,SW,NE, DrawContext, Element, Matrices, Line


class MyLine(Line):
    """Line with experimental connection protocol."""

    def __init__(self, connections):
        super().__init__(connections)
        self.fuzziness = 2
        self.name = base64.b64encode(str(uuid.uuid4()).encode()).decode()[:3]
        self.cant_cars = 15 #capacity
        self.max_percent = 100
        self.min_percent = 0
        self.entry_cars = 0 # if the connection is only one for entry
        self.is_entry = False
        self.is_exit = False
        self.cars_in_exit = 0
        self._saw_message = 'None'
        self.estimated_percentage = 0
        self.write_message()

    def draw_tail(self, context):
        cr = context.cairo
        cr.line_to(0, 0)
        cr.line_to(10, 10)
        cr.stroke()

    def draw(self, context: DrawContext) -> None:
        super().draw(context)
        cr = context.cairo
        cr.set_source_rgb(1,0.3,0.1)
        x_postion = (self._handles[0]._pos.x._value + self._handles[-1]._pos.x._value) / 2
        y_postion = (self._handles[0]._pos.y.value + self._handles[-1]._pos.y.value ) / 2
        text_align(cr,x_postion,y_postion, self._saw_message)
        cr.stroke()

    def write_message(self):
        if not self.is_entry and not self.is_exit:
            self._saw_message = f"Max: {str(self.max_percent)}\n Min: {str(self.min_percent)}\n Cant {str(self.cant_cars)}"
        elif self.is_entry:
            self._saw_message = f"Carros: {str(self.entry_cars)}"
        else:
            self._saw_message = ''
        
    def update_type_path(self,is_entry,is_exit):
        if is_entry and not is_exit:
            self.is_entry = True
            self.is_exit = False
        elif not is_entry and is_exit:
            self.is_entry = False
            self.is_exit = True
        else:
            self.is_entry = False
            self.is_exit = False
        self.write_message()

class Box(Element):
    """An Element has 4 handles (for a start):

    .. code-block:: text

       NW +---+ NE
          |   |
       SW +---+ SE
    """

    def __init__(self, connections, width=10, height=10):
        super().__init__(connections, width, height)

    def draw(self, context):
        c = context.cairo
        nw = self._handles[NW].pos
        c.rectangle(nw.x, nw.y, self.width, self.height)
        if context.hovered:
            c.set_source_rgba(0.8, 0.8, 1, 1)
        else:
            c.set_source_rgba(1, 1, 1, 0.8)
        c.fill_preserve()
        c.set_source_rgb(0, 0, 0.8)
        c.stroke()

class MyNode(Element):
    def __init__(self, connections, width=60, height=60):
        super().__init__(connections, width, height)
        self.radius = self.width / 2
        self.name = base64.b64encode(str(uuid.uuid4()).encode()).decode()[:5]  # Truncate to 5 chars
        self.min_height = self.height
        self.min_width = self.width
    

    def draw(self, context):
        nw = self._handles[NW].pos
        ne = self._handles[NE].pos
        sw = self._handles[SW].pos
        cr = context.cairo
        # // Coordinates:
        xc = (nw.x + ne.x) / 2
        yc = (nw.y + sw.y) / 2
        radius = self.width / 2
        angle1 = 0  * (math.pi/180.0) 
        angle2 = 360 * (math.pi/180.0)
        
        cr.arc (xc, yc, radius, angle1, angle2)
        if context.hovered:
            # cr.set_source_rgba (1, 0.2, 0.2, 0.6)
            cr.set_source_rgba (0.8, 0.2, 0.2, 0.6)
        else:
            cr.set_source_rgba (1, 0.2, 0.2, 0.6)
        cr.fill_preserve ()
        cr.set_source_rgb(0.1,0.1,0.1)
        cr.move_to(xc / 2, yc)
        cr.show_text(self.name)
        cr.stroke ()

    def on_double_click(self, widget, event):
        if event.type == Gtk.EventType.BUTTON_PRESS and event.button == Gtk.BUTTON_PRIMARY and event.get_click_count() == 2:
            print("Double click detected on MyNode!")

    


class Text(Matrices):
    """Simple item showing some text on the canvas."""

    def __init__(self, text=None, plain=False, multiline=False, align_x=1, align_y=-1):
        super().__init__()
        self.text = "Hello" if text is None else text
        self.plain = plain
        self.multiline = multiline
        self.align_x = align_x
        self.align_y = align_y

    def handles(self):
        return []

    def ports(self):
        return []

    def point(self, x, y):
        return 0

    def draw(self, context):
        cr = context.cairo
        if self.multiline:
            text_multiline(cr, 0, 0, self.text)
        elif self.plain:
            cr.show_text(self.text)
        else:
            text_align(cr, 0, 0, self.text, self.align_x, self.align_y)


class Circle(Matrices):
    def __init__(self):
        super().__init__()
        self._handles = [Handle(), Handle()]
        h1, h2 = self._handles
        h1.movable = False

    @property
    def radius(self):
        h1, h2 = self._handles
        p1, p2 = h1.pos, h2.pos
        return ((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2) ** 0.5

    @radius.setter
    def radius(self, r):
        h1, h2 = self._handles
        h2.pos.x = r
        h2.pos.y = r

    def handles(self):
        return self._handles

    def ports(self):
        return []

    def point(self, x, y):
        h1, _ = self._handles
        p1 = h1.pos
        dist = ((x - p1.x) ** 2 + (y - p1.y) ** 2) ** 0.5
        return dist - self.radius

    def draw(self, context):
        cr = context.cairo
        path_ellipse(cr, 0, 0, 2 * self.radius, 2 * self.radius)
        cr.stroke()


def text_align(cr, x, y, text, align_x=0, align_y=0, padding_x=0, padding_y=0):
    """Draw text relative to (x, y).

    x, y - coordinates
    text - text to print (utf8)
    align_x - -1 (top), 0 (middle), 1 (bottom)
    align_y - -1 (left), 0 (center), 1 (right)
    padding_x - padding (extra offset), always > 0
    padding_y - padding (extra offset), always > 0
    """
    if not text:
        return

    x_bear, y_bear, w, h, _x_adv, _y_adv = cr.text_extents(text)
    if align_x == 0:
        x = 0.5 - (w / 2 + x_bear) + x
    elif align_x < 0:
        x = -(w + x_bear) + x - padding_x
    else:
        x = x + padding_x
    if align_y == 0:
        y = 0.5 - (h / 2 + y_bear) + y
    elif align_y < 0:
        y = -(h + y_bear) + y - padding_y
    else:
        y = -y_bear + y + padding_y
    cr.move_to(x, y)
    cr.show_text(text)

def show_line_text(cr, x, y, text):
    if not text: return
    cr.move_to(x, y)
    cr.show_text(text)


def text_multiline(cr, x, y, text):
    """Draw a string of text with embedded newlines.

    cr - cairo context
    x - leftmost x
    y - topmost y
    text - text to draw
    """
    if not text:
        return
    for line in text.split("\n"):
        _x_bear, _y_bear, _w, h, _x_adv, _y_adv = cr.text_extents(text)
        y += h
        cr.move_to(x, y)
        cr.show_text(line)


def path_ellipse(cr, x, y, width, height, angle=0):
    """Draw an ellipse.

    x      - center x
    y      - center y
    width  - width of ellipse  (in x direction when angle=0)
    height - height of ellipse (in y direction when angle=0)
    angle  - angle in radians to rotate, clockwise
    """
    cr.save()
    cr.translate(x, y)
    cr.rotate(angle)
    cr.scale(width / 2.0, height / 2.0)
    cr.move_to(1.0, 0.0)
    cr.arc(0.0, 0.0, 1.0, 0.0, 2.0 * pi)
    cr.restore()
