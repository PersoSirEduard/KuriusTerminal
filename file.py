class File:

    def __init__(self, name, path, params = {}):
        self.name = name
        self.path = path
        self.data = ""

        for key, value in params.items():
            setattr(self, key, value)

    def __str__(self):
        return self.name

    def write(self, data):
        pass

    def read(self):
        pass