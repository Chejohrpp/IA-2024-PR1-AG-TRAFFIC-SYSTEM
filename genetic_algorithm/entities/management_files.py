
class SaveFile():
    def __init__(self, file=None):
        self.file = file

    def save(self, filename):
        # Write msgpack file
        with open(filename, "wb") as outfile:
            # packed = msgpack.packb(self.file)
            # outfile.write(packed)
            pass