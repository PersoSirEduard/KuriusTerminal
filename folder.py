class Folder:

    def __init__(self, tree, name, path, params = {}):
        self.name = name
        self.path = path
        self.type = "folder"
        self.children = {}
        self.count = 0
        self.tree = tree
        
        for key, value in params.items():
            setattr(self, key, value)

    def __str__(self):
        return self.path + self.name

    def addChild(self, child):
        self.children[child.name] = child
        self.count += 1

    
    
def getDirectory(treeDir, path):

    pathRoute = [ p for p in str(path).split("/") if p.strip() != "" ]

    try:
        currentDir = treeDir
        for p in pathRoute:

            currentDir = currentDir.children[p]

            if currentDir.type != "folder":
                 return None
    except:
        return None
    
    return currentDir