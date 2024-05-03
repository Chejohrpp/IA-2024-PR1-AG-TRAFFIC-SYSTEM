from enum import Enum
from typing import Dict
from gaphas.connections import Connections
from genetic_algorithm.entities.node_structure import NodeStructure
from views.model_construction.items import MyLine, MyNode

ENTRY = -1 # hacia TAIL
EXIT = 0 # desde HEAD

class ModelConstructor:
    def __init__(self, items = None, snapshot = None):
            self._items = items
            self._snapshot = snapshot #view.model
            self.set_new_items()
            self._painter_function = None
            self._nodes_entry = []
            self._nodes_exit = []
            # self._nodes_path = []
            self._dict_nodes: Dict[MyNode, NodeStructure] = dict()
            

    def print_items(self):
            print(self._items)

    def set_new_items(self):
            if self._snapshot:
                self._items = list(self._snapshot.get_all_items())
    
    def get_items(self):
            self.set_new_items()
            return self._items
    
    def repaint_items(self):
        self._painter_function()

    def rename_percent(self, item:MyLine, percent):
        item._saw_message = f"{str(percent)}%"

    def update_paths(self,bloke):
        for tuple in bloke:
            item, random_value = tuple
            if isinstance(item, MyLine):
                self.rename_percent(item, random_value)

    def show_directions(self):
                """
                Analyzes the connections of MyLine objects and prints information
                about their direction based on connected items.

                This function iterates through the `self._items` list and checks for
                instances of `MyLine`. For each `MyLine` object:

                1. Retrieves connections using `list(item._connections.get_connections(item=item))`.
                2. Checks the number of connections:
                - If there are 2 connections:
                    - Iterates through connections to identify the 'head' and 'tail'.
                    - Uses connection object's `handle` and `connected.name` attributes to print
                        'hacia' (towards) if the handle is the last element (`item._handles[-1]`)
                        or 'desde' (from) if the handle is the first element (`item._handles[0]`).
                - If there's only 1 connection or no connections:
                    - Prints 'no connected' towards the connected item's name (if there is one).

                Prints messages to the console for each identified 'head' and 'tail' direction.
                """

                for item in self._items:
                    if isinstance(item, MyLine):
                        connections = list(item._connections.get_connections(item=item))
                        num_connections = len(connections)
                        message = ""
                        to_m = ' no connection '
                        from_m = 'no connection '
                        if num_connections > 0:
                            for connection in connections:
                                if connection.handle == item._handles[ENTRY]:
                                    to_m = f" hacia {connection.connected.name}"  # Print 'hacia' + connected name
                                elif connection.handle == item._handles[EXIT]:
                                    from_m = (f"desde {connection.connected.name}")  # Print 'desde' + connected name

                        message = from_m + to_m
                        print (message)           
                    
                    #  elif num_connections <= 1:  # Handle cases with 1 or 0 connections
                    #      if connections:  # Check if there's at least one connection
                    #          connected_name = connections[0].connected.name
                    #          print(f"no connected hacia {connected_name}")  # Print 'no connected' towards connected name
                    #      else:
                    #          print("no connected")  # Print 'no connected' if no connections

    def path_cant_connect(self, item):
        if isinstance(item, MyLine):
            connections = list(item._connections.get_connections(item=item))
            return len(connections)

    "it used to for create the new population in the GA"
    def get_number_paths(self):
        paths = []
        # cant = 0 #deprecated
        for item in self._items:
            if isinstance(item, MyLine):
                  # before see is a really path or a entry/exit
                  if self.path_cant_connect(item) == 2:                       
                    # cant += 1
                    path = {
                         'percent_max' : item.max_percent,
                         'percent_min' : item.min_percent,
                         'key' : item
                    }
                    paths.append(path)
        # path['cant'] = cant
        return paths
    
    def validate_percentages(self, percentages):
        #percentages is the array of tuples
        for tuple in percentages:
            item, random_value = tuple
            if isinstance(item, MyLine):
                item.estimated_percentage = random_value
        new_percentage = []
        for value in self._dict_nodes.values():
            new_percentage += value.normalize_percentages()
        return new_percentage
        

    
    def fill_nodes(self):
         for item in self._items:
              if isinstance(item, MyNode):
                   self._dict_nodes[item] = NodeStructure(item)

                   
    # run 1 time
    def define_node(self):
        self._nodes_entry = []
        self._nodes_exit = []
        # self._dict_nodes: Dict[MyNode, NodeStructure] = dict()

        self.fill_nodes()
        for item in self._items:
              if isinstance(item, MyLine):
                connections = list(item._connections.get_connections(item=item))
                num_connections = len(connections)
                #entry or exit
                if num_connections == 1:
                    connection = connections[0]
                    if connection.handle == item._handles[ENTRY]:
                        # print(f"node de entrada {connection.connected.name}")  # entrada
                        self._nodes_entry.append(connection.connected)
                        self._dict_nodes[connection.connected]._entry = item
                    elif connection.handle == item._handles[EXIT]:
                        # print(f"node de salida {connection.connected.name}")  # Print 'desde' + connected name
                        self._nodes_exit.append(connection.connected)
                        self._dict_nodes[connection.connected]._exit = item
                elif num_connections == 2:
                    node_parent = None
                    node_child = None
                    for connection in connections:
                        if connection.handle == item._handles[ENTRY]:
                            node_child = connection.connected
                        elif connection.handle == item._handles[EXIT]:
                            node_parent = connection.connected
                    # print (f'parent {node_parent.name}')
                    self._dict_nodes[node_parent].add_path(item) #replace? yes, could be different parents
                    self._dict_nodes[node_parent].add_path_dict(node_child,item)
                    self._dict_nodes[node_parent].add_node_goto(self._dict_nodes[node_child])
        # for value in self._dict_nodes.values():
        #      value.print_nodes_connected()
        

    def print_roads(self):
         #Only the nodes of the entry
        for node in self._nodes_entry:
            print(self._dict_nodes[node].send_signal())

    def print_Nodes_max_cars(self):
         for value in self._dict_nodes.values():
            print(value.get_node_name())
            print(value.max_total_cars())
            # value.print_nodes_connected()

    def cant_cars_out(self, bloke):
         # self.rename_percent(item, random_value) #se muestre el nuevo valor
         for item_tuple in bloke:
            item, random_value = item_tuple
            if isinstance(item, MyLine):
                 item.estimated_percentage = random_value
         return self.calulate_road()

    def calulate_road(self):
        cars_out = 0
        for node in self._nodes_entry:
            cars_out +=  self._dict_nodes[node].send_cars(self._dict_nodes[node].get_cars_entry())
        return cars_out
                    
                            
                     
                   
                   
    
                      