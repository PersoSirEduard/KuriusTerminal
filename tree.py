import json
from folder import *
from file import *

class Tree:

    def __init__(self):
        self.currentDir = "/"
        self.name = "/"
        self.children = {}
        self.count = 0

    def __str__(self):
        return self.currentDir

    def addChild(self, child):
        self.children[child.name] = child
        self.count += 1

    # Load the directory tree structure for files and folders
    def load(self, path):
        try:
            with open(path) as file:
                result = json.loads(file.read())

                # Initialize the root folder
                root = self._loadExplore('/', result.get("root").get("files"))
                for content in root: self.addChild(content)

        except Exception as e:
            print(e)
            print("Error: Could not read the tree directory")

    # Recursively load the directory tree structure for files and folders
    def _loadExplore(self, path, rawParent):

        localContent = []

        for name in rawParent: # Loop through the files and folders (by name)
            body = rawParent[name] # Get the body of the current file/folder

            if isinstance(body, dict):

                # Get the attributes of the current file/folder
                attribs = { k: v for k, v in body.items() if k != "files"}

                if body.get("type") == "folder":
                    contents = self._loadExplore(path + name + "/", body.get("files"))
                    
                    # Create a new folder object
                    newFolder = Folder(name, path, attribs)
                    
                    # Add its sub folders and files
                    for content in contents:
                        newFolder.addChild(content)

                    localContent.append(newFolder)

                else:
                    localContent.append(File(name, path, attribs))

        return localContent

    def getCurrentDir(self):
        return self.currentDir
    
    def setCurrentDir(self, path):
        self.currentDir = path

    def getParentPath(self):
        return "/"

    def getFullPath(self):
        return "/"

    def getDirectory(self, path, relativePath = False):
        if str(path).strip() == "/":
            return self
        else:
            return getDirectory(self, path, relativePath)
    
    # Function that gets the file/folder name from its path (i.e. the last element of the path) as a string
    def getPathName(self, path):
        if str(path) != "/":
            return str(path).split("/")[-1]
        return "/"


    """ Note (Eduard): Code needs to be worked on because it is messy and has impractical statements/methods """
    def getTreePath(self, path, maxDepth = 2, _currDepth = 0, showHidden = False, showFullPath = False):

        curr = path
        if showFullPath:
            graph = str(curr)
        else:
            graph = self.getPathName(curr)
        
        keys = list(curr.children.keys())

        for i in range(len(keys)):

            child = curr.children[keys[i]]
            
            # Stop the tree structure at the max depth and do not display hidden files
            if _currDepth >= maxDepth and not showHidden: return graph

            if i + 1 == len(curr.children):
                graph += "\n" + (_currDepth * f"{'│'}\t") + "└"
            else:
                graph += "\n" + (_currDepth * f"{'│'}\t") + "├"

            # Stop the tree structure at the max depth and display hidden files
            if _currDepth >= maxDepth and showHidden:
                graph += "(...)"
                return graph
            
            if hasattr(child, 'children') and child.children != None and len(child.children) > 0:
                graph += self.getTreePath(child, maxDepth, _currDepth + 1, showHidden, showFullPath)
            else:
                if showFullPath:
                    graph += str(self.getDirectory(child))
                else:
                    graph += child.getName().replace("/", "")
        
        return graph
