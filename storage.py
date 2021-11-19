class StorageEntity:

    def __init__(self, name, path, params = {}):
        self.name = name
        self.path = path
        self.params = {}

    def __str__(self):
        return self.getFullPath()

    # Get the parent folder of the file
    def getParentPath(self):
        return self.path

    # Get the name of the file
    def getName(self):
        return self.name

    # Get the full path of the file
    def getFullPath(self):
        return self.path + self.name
