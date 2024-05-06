from functools import partial
import sys

import gi
from math import pi

from genetic_algorithm.entities.model_constructor import ModelConstructor

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject, Gdk

from gaphas import Canvas
from gaphas.view import GtkView
from views.model_construction.items import Box, MyLine, MyNode
from gaphas.guide import GuidePainter
from gaphas.tool import (
    hover_tool,
    item_tool,
    placement_tool,
    view_focus_tool,
    zoom_tool,
    zoom_tools,
)
from gaphas.painter import (
    HandlePainter,
    ItemPainter,
    PainterChain,
)        

from gaphas.connections import Connections
from gaphas.handlemove import ItemHandleMove

css_provider = Gtk.CssProvider()
css_provider.load_from_path('views/model_construction/style/creation.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

def apply_default_tool_set(view):
    view.remove_all_controllers()
    view.add_controller(item_tool())
    view.add_controller(zoom_tool())
    view.add_controller(view_focus_tool())
    view.add_controller(hover_tool())

def apply_painter(view):
    view.painter = (
        PainterChain()
        .append(ItemPainter(view.selection))
        .append(HandlePainter(view))
        .append(GuidePainter(view))
    )
    view.add_controller(item_tool())
    view.add_controller(zoom_tool())

def factory(view, cls):
    """Simple canvas item factory."""

    def wrapper():
        item = cls(view.model.connections)
        view.model.add(item)
        return item

    return wrapper

def apply_placement_tool_set(view, item_type, handle_index):
    def unset_placement_tool(gesture, offset_x, offset_y):
        apply_default_tool_set(view)

    view.remove_all_controllers()
    tool = placement_tool(factory(view, item_type), handle_index)
    tool.connect("drag-end", unset_placement_tool)
    view.add_controller(tool)
    for tool in zoom_tools():
        view.add_controller(tool)
    view.add_controller(view_focus_tool())

# def create_window(w,view,canvas, title, zoom=1.0, model_construction = ModelConstructor ):  # noqa too complex
#     # view = GtkView()

#     apply_default_tool_set(view)
#     apply_painter(view)

#     # w = Gtk.Window()
#     # w.set_title(title)
#     # w.set_default_size(820, 512)
#     h = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)

#     def h_append(b):
#         h.append(b)

#     w.set_child(h)

#     # VBox contains buttons that can be used to manipulate the canvas:
#     v = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)

#     def v_append(b):
#         v.append(b)

#     f = Gtk.Frame()
#     f.set_child(v)
#     h_append(f)

#     v_append(Gtk.Label.new("Agregar:"))

#     b = Gtk.Button.new_with_label("Agregar Nodo")

#     def on_add_box_clicked(_button):
#         apply_placement_tool_set(view, MyNode, 2)

#     b.connect("clicked", on_add_box_clicked)
#     v_append(b)

#     b = Gtk.Button.new_with_label("Agregar Arista")

#     def on_add_line_clicked(_button):
#         apply_placement_tool_set(view, MyLine, -1)

#     b.connect("clicked", on_add_line_clicked)
#     v_append(b)

#     v_append(Gtk.Label.new("Opciones del objeto seleccionado:"))

#     b = Gtk.Button.new_with_label("Eliminar")

#     def on_delete_focused_clicked(_button):
#         if view.selection.focused_item:
#             canvas.remove(view.selection.focused_item)

#             # if isinstance(view.selection.focused_item, MyNode) and hasattr(view.selection.focused_item, 'name'):
#             #     view.selection.focused_item.name = 'New name'
#             #     print(view.selection.focused_item.name)

#     b.connect("clicked", on_delete_focused_clicked)
#     v_append(b)

#     v_append(Gtk.Label.new("Modelo:"))

#     # b = Gtk.Button.new_with_label("Write demo.png")

#     # def on_write_demo_png_clicked(_button):
#     #     assert view.model
#     #     painter = ItemPainter()

#     #     bounding_box = calculate_bounding_box(painter, canvas.get_all_items())

#     #     surface = cairo.ImageSurface(
#     #         cairo.FORMAT_ARGB32, int(bounding_box.width), int(bounding_box.height)
#     #     )
#     #     cr = cairo.Context(surface)
#     #     cr.translate(-bounding_box.x, -bounding_box.y)
#     #     painter.paint(items=list(view.model.get_all_items()), cairo=cr)
#     #     cr.show_page()
#     #     surface.write_to_png("demo.png")

#     # b.connect("clicked", on_write_demo_png_clicked)
#     # v_append(b)

#     # b = Gtk.Button.new_with_label("Write demo.svg")

#     # def on_write_demo_svg_clicked(button):
#     #     assert view.model
#     #     painter = ItemPainter()

#     #     bounding_box = calculate_bounding_box(painter, canvas.get_all_items())

#     #     surface = cairo.SVGSurface(
#     #         "demo.svg", int(bounding_box.width), int(bounding_box.height)
#     #     )
#     #     cr = cairo.Context(surface)
#     #     cr.translate(-bounding_box.x, -bounding_box.y)
#     #     painter.paint(items=list(view.model.get_all_items()), cairo=cr)
#     #     cr.show_page()
#     #     surface.flush()
#     #     surface.finish()

#     # b.connect("clicked", on_write_demo_svg_clicked)
#     # v_append(b)

#     b = Gtk.Button.new_with_label("Finalizado")

#     def on_dump_qtree_clicked(_button, li, model_construction):
        
#         # Obtén la lista de objetos
#         # items = list(canvas.get_all_items())
#         # modelConts = ModelConstructor(items)
#         # if model_construction is not None:
#         if model_construction is None:
#             model_construction = ModelConstructor()
#         # model_construction._items = items
#         model_construction._snapshot = view.model
#         # print(view.model)
#         # print(model_construction)
#         # model_construction.print_items()

#         # Itera sobre cada objeto en la lista
#         # for item in items:
#         #     print ('item: ', item)
#         #     # Verifica si el objeto es una instancia de MyNode y tiene una propiedad width
#         #     if isinstance(item, MyLine) and hasattr(item, '_connections'):
#         # #         # Imprime la anchura del objeto
#         # #         print('tail', item._handles[-1].connectable)
#         #         connections = list(item._connections.get_connections(item=item))
#         #         for connection in connections:
#         #             print(connection)
#         #             print (connection.handle == item._handles[-1])

#         # view._qtree.dump()

#         w.finish_creation(model_construction)

#     on_dump_qtree_clicked_partial = partial(on_dump_qtree_clicked, model_construction=model_construction)
#     b.connect("clicked",on_dump_qtree_clicked_partial , [0])
#     v_append(b)
    
#     # Save the model
#     b = Gtk.Button.new_with_label("Cancelar")

#     b.connect("clicked", w.on_response)
#     v_append(b)

#     # Add the actual View:

#     view.model = canvas
#     view.zoom(zoom)
#     view.set_size_request(150, 120)
#     s = Gtk.ScrolledWindow.new()
#     s.set_hexpand(True)
#     s.set_child(view)
#     h_append(s)

#     w.present()

#     w.connect("destroy", lambda w: app.quit())

#     return w


# def create_canvas(canvas,view):
#     # Draw first gaphas box
#     b1 = MyNode(canvas.connections, 60, 60)
#     b1.matrix.translate(100, 10)
#     canvas.add(b1)

#     b2 = MyNode(canvas.connections, 60, 60)
#     b2.matrix.translate(100, 100)
#     canvas.add(b2)

#     l1 = MyLine(canvas.connections)
#     l1.matrix.translate(90, 80)
#     l1._handles[-1].pos = (40,20)
#     canvas.add(l1)

#     c = Connections()
#     c.connect_item(l1,l1.handles()[0],b2,b2.ports()[0])
#     print(c.get_connection(l1.handles()[0]))

#     ihm = ItemHandleMove(l1,l1.handles()[0],view)
#     ihm.connect(b1._handles[0].pos)

#     return canvas


# app = Gtk.Application.new("org.hrp.traffict_system.creation", 0)


# def main(model_construction):
#     def activate(app,model_construction):
#         c = Canvas()
#         win1 = create_window(c, "Construccion del model", model_construction=model_construction)
#         create_canvas(c)
#         app.add_window(win1)
        
#     # Crear una función parcialmente aplicada con model_construction predefinido
#     activate_with_model = partial(activate, model_construction=model_construction)
    
#     app.connect("activate", activate_with_model)
#     app.run()


# if __name__ == "__main__":
#         main()


class CreationWindow(Gtk.ApplicationWindow):

    __gsignals__ = {
        'window-closed': (GObject.SignalFlags.RUN_LAST, GObject.TYPE_NONE, (object,))
    }

    def __init__(self,model, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.set_default_size(850, 710)
        self.set_title("Creacion")
        self.model_construction = model
        self.view = GtkView()
        if isinstance(self.model_construction, ModelConstructor):
            c = self.model_construction._snapshot
        else : 
            c = Canvas()
        #create_window(self,self.view, c, "Construccion del model", model_construction=self.model_construction)
        self.create_window(c)
        self.on_activate()

    def create_window(self,canvas):
        apply_default_tool_set(self.view)
        apply_painter(self.view)
        h = Gtk.Box.new(Gtk.Orientation.HORIZONTAL, 6)
        def h_append(b):
            h.append(b)

        self.set_child(h)
        v = Gtk.Box.new(Gtk.Orientation.VERTICAL, 6)
        def v_append(b):
            v.append(b)
        f = Gtk.Frame()
        f.set_child(v)
        h_append(f)

        v_append(Gtk.Label.new("Agregar:"))

        b = Gtk.Button.new_with_label("Agregar Cruce")
        def on_add_box_clicked(_button):
            apply_placement_tool_set(self.view, MyNode, 2)
        b.connect("clicked", on_add_box_clicked)
        v_append(b)

        b = Gtk.Button.new_with_label("Agregar Camino")
        def on_add_line_clicked(_button):
            apply_placement_tool_set(self.view, MyLine, -1)
        b.connect("clicked", on_add_line_clicked)
        v_append(b)

        v_append(Gtk.Label.new("Opciones del objeto seleccionado:"))

        b = Gtk.Button.new_with_label("Eliminar")
        def on_delete_focused_clicked(_button):
            if self.view.selection.focused_item:
                canvas.remove(self.view.selection.focused_item)
        b.connect("clicked", on_delete_focused_clicked)
        v_append(b)

        b = Gtk.Button.new_with_label("Caracteristicas")
        def on_change_features_focused_clicked(_button):
            item = self.view.selection.focused_item
            if item is not None:
                # print("feature")
                if isinstance(item, MyLine):
                    is_visible = fb.get_visible()
                    #setter
                    if item.is_entry : radio_is_entry.set_active(True)
                    if item.is_exit : radio_is_exit.set_active(True)
                    if not item.is_exit and not item.is_entry: radio_is_path.set_active(True)
                    if not is_visible:
                        cant_cars.set_text(str(item.cant_cars))
                        max_percent.set_text(str(item.max_percent))
                        min_percent.set_text(str(item.min_percent))
                        #validate first
                        entry_cars.set_text(str(item.entry_cars))
                    #Getters
                    if is_visible:
                        item.cant_cars = int(cant_cars.get_text())
                        item.max_percent = int(max_percent.get_text())
                        item.min_percent = int(min_percent.get_text())
                        #validate before
                        item.entry_cars = int(entry_cars.get_text())
                    fb.set_visible(not is_visible)
                    item.write_message()
                    _button.set_label('Hecho' if not is_visible else 'Caracteristicas')

        b.connect("clicked", on_change_features_focused_clicked)
        v_append(b)

        fb = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        fb.set_spacing(6)
        fb.set_css_classes(['box-feature'])
        fb.set_visible(False)
        v_append(fb)

        def fb_append(widget):
            fb.append(widget)

        fbradio = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        def fbradio_append(widget):
            fbradio.append(widget)
        fb_append(fbradio)

        fbfet = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        fbfet.set_visible(False)
        def fbfet_append(widget):
            fbfet.append(widget)
        fb_append(fbfet)

        fbentry = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        fbentry.set_visible(False)
        def fbentry_append(widget):
            fbentry.append(widget)
        fb_append(fbentry)

        #Features for the current item
        #radio buttons
        def type_of_path(radio,event):
            # print(event)
            item = self.view.selection.focused_item
            if isinstance(item, MyLine):
                if radio_is_entry.get_active():
                    fbentry.set_visible(True)
                    fbfet.set_visible(False)
                    item.update_type_path(True, False)
                elif  radio_is_path.get_active():
                    fbfet.set_visible(True)
                    fbentry.set_visible(False)
                    item.update_type_path(False, False)
                else:
                    fbfet.set_visible(False)
                    fbentry.set_visible(False)
                    item.update_type_path(False, True)
            
        radio_is_entry = Gtk.CheckButton(label="Es entrada")
        radio_is_entry.connect("toggled", type_of_path, "entry")
        fbradio_append(radio_is_entry)
        radio_is_path = Gtk.CheckButton(label="Es camino")
        radio_is_path.set_group(radio_is_entry)
        radio_is_path.connect("toggled", type_of_path, "path")
        fbradio_append(radio_is_path)
        radio_is_exit = Gtk.CheckButton(label="Es salida")
        radio_is_exit.set_group(radio_is_entry)
        radio_is_exit.connect("toggled", type_of_path, "exit")
        fbradio_append(radio_is_exit)
        #Line
        fbfet_append(Gtk.Label.new("Cantidad Carros:"))
        cant_cars = Gtk.Entry.new()
        fbfet_append(cant_cars)
        fbfet_append(Gtk.Label.new("Porcentaje max:"))
        max_percent = Gtk.Entry.new()
        fbfet_append(max_percent)
        fbfet_append(Gtk.Label.new("Porcentaje Min:"))
        min_percent = Gtk.Entry.new()
        fbfet_append(min_percent)
        #Only if is a entry of cars
        fbentry_append(Gtk.Label.new("Entrada de carros:"))
        entry_cars = Gtk.Entry.new()
        fbentry_append(entry_cars)
        #What happens if is a exit?
        #Node
        #create a box
        #Append def
        #label and entry for the name

        v_append(Gtk.Label.new("Modelo:"))

        b = Gtk.Button.new_with_label("Finalizado")

        def on_dump_qtree_clicked(_button, li, model_construction):
            if model_construction is None:
                model_construction = ModelConstructor()
            model_construction._snapshot = self.view.model
            self.finish_creation(model_construction)

        on_dump_qtree_clicked_partial = partial(on_dump_qtree_clicked, model_construction=self.model_construction)
        b.connect("clicked",on_dump_qtree_clicked_partial , [0])
        v_append(b)

        # Add the actual View:

        self.view.model = canvas
        self.view.zoom(1)
        self.view.set_size_request(150, 120)
        s = Gtk.ScrolledWindow.new()
        s.set_hexpand(True)
        s.set_child(self.view)
        h_append(s)
        
    def on_response(self, dialog):
        self.close()
        self.hide()
        self.destroy()  # Then destroy it
        # self.emit("window-closed", self.model)

    def finish_creation(self, model_construction):
        self.emit("window-closed", model_construction)
        self.close()
        self.destroy()  # Then destroy it

    def on_activate(self):
        self.present()

