import sys
import gi

from genetic_algorithm.algorithm import GeneticAlgorithm, typesCriteriaFinalization
from genetic_algorithm.entities.management_files import SaveFile
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

        self.box2.set_css_classes(['box2'])
        self.box2.set_spacing(26)

        self.box3.set_css_classes(['model-creation'])

        self.button = Gtk.Button(label="Editar modelo")
        self.box2.append(self.button)
        self.button.connect('clicked', self.open_model_contruction)

        self.switch_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.box2.append(self.switch_box)

        self.switch = Gtk.Switch()
        self.switch.set_active(True)
        self.switch.connect('state-set', self.toogle_handle_switch)

        self.switch_box.append(self.switch)

        # self.label = Gtk.Label(label='self.label a switch')
        # self.label.set_css_classes(['title'])
        # self.switch_box.append(self.label)
        # self.switch_box.set_spacing(12)

        #population variable
        self.population_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.population_box.set_css_classes(['entry'])
        self.population_box.set_spacing(6)
        self.box2.append(self.population_box)

        self.label = Gtk.Label(label='Tamaño Poblacion')
        self.label.set_css_classes(['title'])
        self.population_box.append(self.label)

        self.size_population = Gtk.Entry.new()
        self.population_box.append(self.size_population)

        #mutations rate
        self.label = Gtk.Label(label='Mutacion ')
        self.label.set_css_classes(['title'])
        self.box2.append(self.label)

        self.mutation_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.mutation_box.set_css_classes(['entry'])
        self.mutation_box.set_spacing(6)
        self.box2.append(self.mutation_box)

        self.mutation_rate_x = Gtk.Entry.new()
        self.mutation_rate_x.set_placeholder_text("X")
        self.mutation_box.append(self.mutation_rate_x)

        self.mutation_box_y = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL)
        self.mutation_box_y.set_css_classes(['entry'])
        self.mutation_box_y.set_spacing(6)
        self.box2.append(self.mutation_box_y)

        self.label = Gtk.Label(label='cantidad de mutacion ')
        self.label.set_css_classes(['title'])
        self.mutation_box.append(self.label)

        self.label = Gtk.Label(label='por cada ')
        self.label.set_css_classes(['title'])
        self.mutation_box_y.append(self.label)

        self.mutation_rate_y = Gtk.Entry.new()
        self.mutation_rate_y.set_placeholder_text("Y")
        self.mutation_box_y.append(self.mutation_rate_y)

        self.label = Gtk.Label(label='generaciones ')
        self.label.set_css_classes(['title'])
        self.mutation_box_y.append(self.label)

        #Criteria of finalization
        self.label = Gtk.Label(label='Criterio de finalizacion')
        self.label.set_css_classes(['title'])
        self.box2.append(self.label)

        self.radio_generations = Gtk.CheckButton(label="Número de generaciones")
        # self.radio_generations.set_active(True)
        self.box2.append(self.radio_generations)

        self.radio_percent = Gtk.CheckButton(label="Porcentaje de eficiencia")
        self.radio_percent.set_group(self.radio_generations)
        self.box2.append(self.radio_percent)

        self.radio_generations.connect("toggled", self.radio_toggled_finalization, "test")

        self.slider = Gtk.Scale()
        self.slider.set_digits(0)  # Number of decimal places to use
        self.slider.set_range(0, 100)
        self.slider.set_draw_value(True)  # Show a label with current value
        self.slider.set_value(0)  # Sets the current value/position
        self.slider.connect('value-changed', self.slider_changed)
        self.box2.append(self.slider)
        self.slider.set_visible(False)

        self.number_generation_entry = Gtk.Entry.new()
        self.number_generation_entry.set_visible(False)
        self.box2.append(self.number_generation_entry)

        #Stop the algorithm
        self.btn_stop = Gtk.Button(label="Detener la ejecucion")
        self.box2.append(self.btn_stop)

        #Header Bar
        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)

        # File Dialog
        self.open_dialog = Gtk.FileDialog.new()
        self.open_dialog.set_title("open file dialog")

        f = Gtk.FileFilter()
        f.set_name("pgats files")
        f.add_pattern("*.py")  # Filter based on the .pgats extension
        f.add_pattern("*.pgats")  # Filter based on the .pgats extension

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

        #Button Bar
        self.button_bar = Gtk.Button(label="button bar")
        self.button_bar.set_icon_name("document-open-symbolic")
        self.button_bar.connect('clicked', self.show_open_dialog)
        self.header.pack_start(self.button_bar)

        # run the app acton
        action = Gio.SimpleAction.new('run_model', None)
        action.connect("activate", self.run_model)
        self.add_action(action)
        menu.append('Ejecutar ', 'win.run_model')

        # Save model
        action = Gio.SimpleAction.new('save_model', None)
        action.connect("activate", self.save_model)
        self.add_action(action)
        menu.append('Guardar el modelo', 'win.save_model')

        #properties
        GLib.set_application_name('Traffic Management')

        # Create an action to run a *show about dialog* function we will create 
        action = Gio.SimpleAction.new("about", None)
        action.connect("activate", self.show_about_window)
        self.add_action(action)
        menu.append('acerca de', 'win.about')

        # self.resize_box3 = Gtk.SizeGroup.new(Gtk.SizeGroupMode.BOTH)

        self.canvas = Canvas()
        self.show_space_traffic_model()

    def run_model(self,action, param):
        print("Running model")
        if self.traffic_model is not None:
        # Set the parameters for the Genetic Algorithm
            size_population = int(self.size_population.get_text())
            mutation_rate_x = int(self.mutation_rate_x.get_text())
            mutation_rate_y = int(self.mutation_rate_y.get_text())
            type_criteria_finalization = typesCriteriaFinalization.NUMBER_GENERATION
            gen_a = GeneticAlgorithm(size_population, mutation_rate_x,
                                     mutation_rate_y, type_criteria_finalization,
                                     self.traffic_model)
            gen_a.training()

    def radio_toggled_finalization(self, radio, event):
        if self.radio_generations.get_active():
            self.slider.set_visible(False)
            self.number_generation_entry.set_visible(True)
        else :
            self.slider.set_visible(True)
            self.number_generation_entry.set_visible(False)

    def save_model(self, action, param):
        self.open_dialog.save(self, None, self.save_model_callback)

    def save_model_callback(self, dialog, result):
        try:
            file = dialog.save_finish(result)
            if file is not None:
                self.save_file(file)
        except GLib.Error as error:
            print(f"Error to save file: {error.message}")


    def save_file(self, file):

        # serialized_data = msgpack.packb(self.traffic_model, use_bin_type=True)
        text = 'some text file'
        bytes = GLib.Bytes.new(text.encode('utf-8'))
        # bytes = GLib.Bytes.new(self.traffic_model)

        # Start the asynchronous operation to save the data into the file
        file.replace_contents_bytes_async(bytes,
                                        None,
                                        False,
                                        Gio.FileCreateFlags.NONE,
                                        None,
                                        self.save_file_complete)
        
    def save_file_complete(self, file, result):
        res = file.replace_contents_finish(result)
        info = file.query_info("standard::display-name",
                            Gio.FileQueryInfoFlags.NONE)
        if info:
            display_name = info.get_attribute_string("standard::display-name")
            print(file.get_path())
        else:
            display_name = file.get_basename()
            print("basename")
        # save = SaveFile(self.traffic_model)
        # save.save(file.get_path())
        if not res:
            print(f"Unable to save {display_name}")


    def show_space_traffic_model(self):
        view = GtkView()
        view.model = self.canvas
        view.zoom(1.4)
        s = Gtk.ScrolledWindow.new()
        s.set_hexpand(True)
        s.set_child(view)
        f = Gtk.Frame.new()
        f.set_size_request(560, 640)
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
            self.traffic_model.show_directions()
            self.traffic_model.repaint_items()

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
        self.traffic_model._painter_function = self.show_traffic_model_canvas

    def toogle_handle_switch(self, switch, state):
         print(f"the switch it's {'on' if state else 'off'}")


class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)
        self.set_accels_for_action('win.save_model', ['<Ctrl><Shift>s'])
        self.set_accels_for_action('win.run_model', ['<Ctrl><Shift>r'])
        sm = self.get_style_manager()
        sm.set_color_scheme(Adw.ColorScheme.PREFER_DARK)

    def on_activate(self, app):
        self.win = MainWindow(application=app)
        self.win.present()

if __name__ == "__main__":
    app = MyApp(application_id="com.hrp.TrafficManagement")
    app.run(sys.argv)
