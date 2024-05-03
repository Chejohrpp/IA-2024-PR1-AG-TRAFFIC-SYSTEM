import random
from typing import Dict
from views.model_construction.items import MyNode, MyLine

class NodePath:
    def __init__(self,node: MyNode, path: MyLine):
        self.node: MyNode = node
        self.path: MyLine = path

class NodeStructure:
    def __init__(self, node: MyNode):
        self._node: MyNode = node
        self._nodes_connected: NodeStructure = []
        self._entry = None
        self._exit = None
        self._paths = []
        self._dict_paths: Dict[MyNode, MyLine] = dict()

    def get_cars_entry(self):
        if isinstance(self._entry, MyLine):
            return self._entry.entry_cars
        return 0


    def add_path_dict(self, node_child: MyNode, path: MyLine):
        self._dict_paths[node_child] = path

    def max_total_cars(self):
        cant_max = 0
        for path in self._paths:
            if isinstance(path, MyLine):
                cant_max += path.cant_cars
        return cant_max
    
    def normalize_percentages(self):
        normalized_percentages = []
        total_sum = 0
        for paths in self._dict_paths.values():
            total_sum += paths.estimated_percentage
        # if total_sum != 100:
        if self._exit: #si el nodo tiene una salida
            if total_sum < 100:
                total_sum = 100 
            else: #si se pasa de 100%
                total_sum += random.randint(0, 100)
        if total_sum == 0 and len(self._dict_paths) == 1:
            total_sum = 100
        for paths in self._dict_paths.values():
            normalized_percentages.append((paths, round((paths.estimated_percentage / total_sum) * 100, 2)) )
        return normalized_percentages

    def get_node_name(self):
        return self._node.name

    def send_signal(self, visited_nodes=None):
        if visited_nodes is None:
            visited_nodes = set()  # Initialize visited nodes set
        paths = []
        for child in self._nodes_connected:
             # Check if child has already been visited to detect loops
            if child in visited_nodes:
                continue  # Skip child if already visited
            # Add current node to visited nodes set
            visited_nodes.add(child)

            arrays_childs = child.send_signal() #arrays of arrays

            curr_name = ''
            if self._entry:
                curr_name = self.get_node_name() + ' --> '
            node_name =  curr_name + child.get_node_name()
            the_path = node_name + ' --> '

            for arr in arrays_childs:
                if isinstance(arr,list):
                    for ar in arr:
                        paths.append(the_path + ar)
                else: # when is exit or no road
                    paths.append(the_path + arr)
        # Check for exit or no paths
        if self._exit:
            return paths + ['exit']
        elif self._exit == None and len(self._nodes_connected) == 0:
            return paths + ['no roads']
        else:
            return paths  # No exit or child nodes found
        
    def send_cars(self,cars_entry):
        # paths = []
        exits_cars = 0
        aux_exit_cars_entry = cars_entry
        for child in self._nodes_connected:            
            
            my_line = self._dict_paths[child._node]
            cant_cars_allowed = my_line.cant_cars
            percent = my_line.estimated_percentage

            # Integer division for calculating the number of cars
            cars_percent = int(cars_entry * (percent / 100))
            aux_exit_cars_entry = aux_exit_cars_entry - cars_percent #line not necessarily??

            cars_sendings = cars_percent
            if cant_cars_allowed < cars_sendings:
                cars_sendings = cant_cars_allowed

            exits_cars += child.send_cars(cars_sendings) #arrays of arrays
            # curr_name = ''
            # if self._entry:
            #     curr_name = self.get_node_name() + ' --> '
            # node_name =  curr_name + child.get_node_name()
            # the_path = node_name + ' --> '

            # for arr in arrays_childs:
            #     paths.append(the_path + arr)
            
        # Check for exit or no paths
        if self._exit:
            return exits_cars + aux_exit_cars_entry # + ['exit']
        elif self._exit == None and len(self._nodes_connected) == 0:
            return exits_cars + 0 # + ['no roads']
        else:
            return exits_cars  # No exit or child nodes found

            
    def add_node_goto(self, item):
        self._nodes_connected.append(item)

    def add_path(self, path):
        self._paths.append(path)

    def print_nodes_connected(self):
        print(f"{'entry ' if self._entry else ' '}parent -> {self._node.name}")
        for child in self._nodes_connected:
            print(f"   ---> {child._node.name}")
        print(f"   ---> exit") if self._exit else None
