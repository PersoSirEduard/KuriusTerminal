from utils import formatPath
from storage import StorageEntity
from utils import hasPermission
from datetime import datetime

class Folder(StorageEntity):

    def __init__(self, name, path, params = {}):
        self.params = {}
        for key, value in params.items():
            setattr(self, key, value)

        self.name = name
        self.path = path
        self.children = {}
        self.count = 0 # number of children

    # Add content to the folder
    def addChild(self, child):
        self.children[child.name] = child
        self.count += 1

    # Get a file in the folder
    def getFile(self, fileName):
        try:
            return self.children[fileName]
        except Exception as e:
            return None
    
def getDirectory(treeDir, path, relativePath = False, user = None):

    if relativePath:
        path = formatPath(treeDir, path)

    pathRoute = [ p for p in str(path).split("/") if p.strip() != "" ]

    currentDir = treeDir
    try:
        for p in pathRoute:

            currentDir = currentDir.children[p]

            if not isinstance(currentDir, Folder):
                return None

            if hasattr(currentDir, "permission"):
                if not hasPermission(user, currentDir.permission):
                    return None
            
            if hasattr(currentDir, "availability"):
                if not datetime.strptime(currentDir.availability[0], "%Y-%m-%d %H:%M:%S") <= treeDir.env.getSystemTime() <= datetime.strptime(currentDir.availability[1], "%Y-%m-%d %H:%M:%S"):
                    return None
    except:
        return None
    
    return currentDir