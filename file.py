from folder import getDirectory
from storage import StorageEntity
from utils import formatPath
from io import BytesIO
from datetime import datetime
from utils import hasPermission

class File(StorageEntity):

    def __init__(self, name, path, params = {}):

        self.data = ""
        self.params = {}
        for key, value in params.items():
            setattr(self, key, value)

        self.name = name
        self.path = path

    def write(self, data):
        self.data = data

    def read(self, mode="r", limit=True):
        
        # Read from data
        if self.data != "":
            if mode == "rb":
                return BytesIO(self.data)
            else:
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

def getFile(treeDir, path, relativePath = False, user = None):

    try:

        if relativePath:
            path = formatPath(treeDir, path)

        pathRoute = [ p for p in str(path).split("/") if p.strip() != "" ]

        if len(pathRoute) > 0:
            fileName = pathRoute[-1]
            parent = getDirectory(treeDir, '/'.join(pathRoute[:-1]))
            file = parent.children.get(fileName)
            
            if hasattr(file, "permission"):
                if not hasPermission(user, file.permission):
                    return None
            
            if hasattr(file, "availability"):
                if not datetime.strptime(file.availability[0], "%Y-%m-%d %H:%M:%S") <= treeDir.env.getSystemTime() <= datetime.strptime(file.availability[1], "%Y-%m-%d %H:%M:%S"):
                    return None
            
            return file
        
    except Exception as e:
        print(e)
        return None
    