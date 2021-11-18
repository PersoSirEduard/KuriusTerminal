from folder import getDirectory
from utils import formatPath

class File:

    def __init__(self, name, path, params = {}):
        self.name = name
        self.path = path
        self.data = ""

        for key, value in params.items():
            setattr(self, key, value)

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

    def write(self, data):
        pass

    def read(self, mode="r", limit=True):
        
        # Read from data
        if self.data != "":
            return self.data
        # Read from cache
        elif hasattr(self, "cache"):
            try:
                contents = open("cache/" + self.cache, mode).read()

                # Respect discord's max message length
                if limit:
                    if len(contents) > 2000:
                        return contents[:1900] + "\n(...)"
                    else:
                        return contents
                else:
                    return contents

            except Exception as e:
                print(e)
                return None
        # No data
        else:
            return None

def getFile(treeDir, path, relativePath = False):

    try:

        if relativePath:
            path = formatPath(treeDir, path)

        pathRoute = [ p for p in str(path).split("/") if p.strip() != "" ]

        if len(pathRoute) > 0:
            fileName = pathRoute[-1]
            parent = getDirectory(treeDir, '/'.join(pathRoute[:-1]))
            return parent.children.get(fileName)
        
    except Exception as e:
        print(e)
        return None
    