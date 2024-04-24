# Import items from ghapas

from views.model_construction.items import MyLine


class ModelConstructor:
        def __init__(self, items = None, snapshot = None):
                self._items = items
                self._snapshot = snapshot
                self.set_new_items()

        def print_items(self):
                print(self._items)

        def set_new_items(self):
              if self._snapshot:
                    self._items = list(self._snapshot.get_all_items())
        
        def get_items(self):
              self.set_new_items()
              return self._items

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
                                 if connection.handle == item._handles[-1]:
                                     to_m = f" hacia {connection.connected.name}"  # Print 'hacia' + connected name
                                 elif connection.handle == item._handles[0]:
                                     from_m = (f"desde {connection.connected.name}")  # Print 'desde' + connected name

                         message = from_m + to_m
                         print (message)           
                        
                        #  elif num_connections <= 1:  # Handle cases with 1 or 0 connections
                        #      if connections:  # Check if there's at least one connection
                        #          connected_name = connections[0].connected.name
                        #          print(f"no connected hacia {connected_name}")  # Print 'no connected' towards connected name
                        #      else:
                        #          print("no connected")  # Print 'no connected' if no connections
