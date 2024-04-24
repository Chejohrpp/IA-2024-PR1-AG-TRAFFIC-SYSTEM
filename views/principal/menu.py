import sys
import gi

from genetic_algorithm.entities.model_constructor import ModelConstructor
from views.model_construction.creation import CreationWindow, create_canvas
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gdk, GLib, Gio

from gaphas import Canvas
from gaphas.view import GtkView

css_provider = Gtk.CssProvider()
css_provider.load_from_path('views/principal/style/style_menu.css')
Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)

class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = kwargs['application']
        self.traffic_model = None
        # Things will go here
        self.set_default_size(820, 512)
        self.set_title("Menu")

        self.box1 = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL) # ADD IN A LINE
        self.box2 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL) # ADD IN A ROWS
        self.box3 = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)

        self.set_child(self.box1)
        self.box1.append(self.box2)
        self.box1.append(self.box3)

        self.box2.set_spacing(26)

        self.box3.set_css_classes(['model-creation'])

        self.button = Gtk.Button(label="Create modelo")
        self.box2.append(self.button)
        self.button.connect('clicked', self.open_model_contruction)

        self.check = Gtk.CheckButton(label="any goodBye")
        self.check.set_active(True)
        self.box2.append(self.check)


        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2.append(self.switch_box)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        self.switch.connect('state-set', self.toogle_handle_switch)

        self.switch_box.append(self.switch)

        self.label = Gtk.Label(label='self.label a switch')
        self.label.set_css_classes(['title'])
        self.switch_box.append(self.label)
        self.switch_box.set_spacing(12)

        self.slider = Gtk.Scale()
        self.slider.set_digits(0)  # Number of decimal places to use
        self.slider.set_range(0, 100)
        self.slider.set_draw_value(True)  # Show a label with current value
        self.slider.set_value(0)  # Sets the current value/position
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)

        #Header Bar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        self.button_bar = Gtk.Button(label="button bar")
        self.button_bar.set_icon_name("document-open-symbolic")
        self.button_bar.connect('clicked', self.show_open_dialog)
        self.header.pack_start(self.button_bar)


        # File Dialog

        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("Open images")

        f = Gtk.FileFilter()
        f.set_name("Image files")
        f.add_mime_type("image/jpeg")
        f.add_mime_type("image/png")

        filters = Gio.ListStore.new(Gtk.FileFilter)  # Create a ListStore with the type Gtk.FileFilter
        filters.append(f)  # Add the file filter to the ListStore. You could add more.

        self.open_dialog.set_filters(filters)
        self.open_dialog.set_default_filter(f)


        #Create a new action
        action = Gio.SimpleAction.new('something',None)
        action.connect('activate', self.print_something)
        self.add_action(action)

        #New menu wich contains that action
        menu = Gio.Menu.new()
        menu.append('do something', 'win.something')

        # Create a popover
        self.popover = Gtk.PopoverMenu()
        self.popover.set_menu_model(menu)

        #Menu button
        self.menu_button = Gtk.MenuButton()
        self.menu_button.set_popover(self.popover)
        self.menu_button.set_icon_name('open-menu-symbolic')

        #add into the header
        self.header.pack_start(self.menu_button)

        #properties
        GLib.set_application_name('Traffic Management')

        # Create an action to run a *show about dialog* function we will create 
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about_window)
        self.add_action(action)

        menu.append('about', 'win.about')

        self.canvas = Canvas()

        self.show_space_traffic_model()


    def show_space_traffic_model(self):
        view = GtkView()
        view.model = self.canvas
        view.zoom(1.4)
        s = Gtk.ScrolledWindow.new()
        s.set_hexpand(True)
        s.set_child(view)
        f = Gtk.Frame.new()
        f.set_size_request(400, 500)
        f.set_child(s)
        self.box3.append(f)

    def show_traffic_model_canvas(self):
        if isinstance(self.traffic_model, ModelConstructor):
            for item in list(self.canvas.get_all_items()):
                self.canvas.remove(item)
            for item in self.traffic_model.get_items():
                self.canvas.add(item)

    def show_about(self, action, param):
        self.about = Gtk.AboutDialog()
        self.about.set_transient_for(self)  # Makes the dialog always appear in from of the parent window
        self.about.set_modal(True)  # Makes the parent window unresponsive while dialog is showing

        self.about.set_authors(["Chejohrpp"])
        self.about.set_copyright("Copyright 2024 hrp")
        # self.about.set_license_type(Gtk.License.GPL_3_0)
        self.about.set_website("https://github.com/Chejohrpp")
        self.about.set_website_label("github")
        self.about.set_version("0.79")
        self.about.set_logo_icon_name("emoji-travel-symbolic")  # The icon will need to be added to appropriate location
                                                 # E.g. /usr/share/icons/hicolor/scalable/apps/org.example.example.svg
        self.about.set_visible(True)

    def show_about_window(self, action, param):
        dialog = Adw.AboutWindow(transient_for=self.app.get_active_window()) 
        dialog.set_application_name("Traffic Management") 
        dialog.set_version("1.2") 
        dialog.set_developer_name("HRP") 
        dialog.set_license_type(Gtk.License(Gtk.License.GPL_3_0)) 
        dialog.set_comments("Codigo fuente") 
        dialog.set_website("https://github.com/Chejohrpp")  
        dialog.set_copyright("© 2024 HRP") 
        dialog.set_developers(["HRP"]) 
        dialog.set_application_icon("emoji-travel-symbolic") # icon must be uploaded in ~/.local/share/icons or /usr/share/icons
        dialog.set_visible(True)

    def print_something(self, action, param):
        if isinstance(self.traffic_model, ModelConstructor):
            # print(self.traffic_model)
            self.traffic_model.show_directions()

    def show_open_dialog(self, button):
        self.open_dialog.open(self, None, self.open_dialog_open_callback)

    def open_dialog_open_callback(self, dialog, result):
        try:
            file = dialog.open_finish(result)
            if file is not None:
                print(f"File path is {file.get_path()}")
                # Handle loading file from here
        except GLib.Error as error:
            print(f"Error opening file: {error.message}")

    def slider_changed(self, slider):
        print(int(slider.get_value()))

    def hello(self, button):
        print("Hello World")
        if self.check.get_active():
                print("Goodbye world!")
                self.close()
    
    def open_model_contruction(self, button):
        creation_window = CreationWindow(self.traffic_model,application=self.app)
        creation_window.set_transient_for(self)
        creation_window.set_modal(True)
        creation_window.connect("window-closed", self.on_creation_window_closed)
        # creation_window.present()

    def on_creation_window_closed(self, creation_window, model_construction=None):
        # print("Mensaje recibido de la ventana de creación:", model_construction)
        self.traffic_model = model_construction
        self.show_traffic_model_canvas()

    def toogle_handle_switch(self, switch, state):
         print(f"the switch it's {'on' if state else 'off'}")


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.hrp.TrafficManagement")
    app.run(sys.argv)
