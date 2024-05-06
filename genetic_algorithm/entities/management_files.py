import pickle
from enum import Enum
class SaveFile:
    def __init__(self, file=None):
        self.file = file

    def save(self, filename):
        # Write msgpack file
        with open(filename, "wb") as outfile:
            pickle.dump(self.file, outfile, protocol=4)

class typeItem(Enum):
    MyLine = 1
    MyNode = 2

class SaveFileModelConstructor:
    def __init__(self, items_dict):
        self.items_dict: dict = items_dict

    def print_items(self):
        for value in self.items_dict.values():
            if isinstance(value, list):
                for item in value:
                    print(item)

class LoadFile:
    def __init__(self, file_path=''):
        self.file_path = file_path
    
    def load(self):
        with open(self.file_path, 'rb') as file:
            loaded_data = pickle.load(file)
        return loaded_data

