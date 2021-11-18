from utils import formatPath

class Folder:

    def __init__(self, name, path, params = {}):
        self.name = name
        self.path = path
        self.children = {}
        self.count = 0 # number of children
        
        for key, value in params.items():
            setattr(self, key, value)

    def __str__(self):
        return self.getFullPath()

    # Add content to the folder
    def addChild(self, child):
        self.children[child.name] = child
        self.count += 1

    # Get the parent folder of the folder
    def getParentPath(self):
        return self.path
    
    # Get the name of the folder
    def getName(self):
        return self.name

    # Get full path of the folder
    def getFullPath(self):
        return self.path + self.name

    # Get a file in the folder
    def getFile(self, fileName):
        try:
            return self.children[fileName]
        except Exception as e:
            return None
    
def getDirectory(treeDir, path, relativePath = False):

    if relativePath:
        path = formatPath(treeDir, path)

    pathRoute = [ p for p in str(path).split("/") if p.strip() != "" ]

    currentDir = treeDir
    try:
        for p in pathRoute:

            currentDir = currentDir.children[p]

            if not isinstance(currentDir, Folder):
                return None
    except:
        return None
    
    return currentDir