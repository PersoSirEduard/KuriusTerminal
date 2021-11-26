import json
from folder import *
from file import *
from vault import Vault, encrypt
from inspect import ismethod
from environment import *

class Tree:

    def __init__(self):
        self.currentDir = "/"
        self.name = "/"
        self.children = {}
        self.count = 0
        self.env = EnvironmentManager()

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
                root = _loadExplore('/', result.get("root").get("files"))
                for content in root: self.addChild(content)

        except Exception as e:
            print(e)
            print("Error: Could not read the tree directory")

    def getCurrentDir(self):
        return self.currentDir
    
    def setCurrentDir(self, path):
        self.currentDir = path

    def getParentPath(self):
        return "/"

    def getFullPath(self):
        return "/"

    def getDirectory(self, path, relativePath = False, user = None):
        if str(path).strip() == "/":
            return self
        else:
            return getDirectory(self, path, relativePath, user)
    
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
                    if isinstance(child, Vault):
                        graph += child.getName() + " (locked)"
                    else:
                        graph += child.getName().replace("/", "")
        
        return graph

# Recursively load the directory tree structure for files and folders
def _loadExplore(path, rawParent):
    localContent = []

    for name in rawParent: # Loop through the files and folders (by name)
        body = rawParent[name] # Get the body of the current file/folder

        if isinstance(body, dict):

            # Get the attributes of the current file/folder
            attribs = { k: v for k, v in body.items() if k != "files"}

            # Check whether the object should turn into a vault
            toLock = False
            password = "default"

            if "locked" in attribs and attribs.get("locked"):
                
                toLock = True
                attribs.pop("locked")

                # Get or create password
                if "password" in attribs:
                    password = attribs.get("password")
                    if password.strip() == "": password = "default"
                    attribs.pop("password")
                

            if body.get("type") == "folder":
                contents = _loadExplore(path + name + "/", body.get("files"))
                
                # Create a new folder object
                newFolder = Folder(name, path, attribs)
                
                # Add its sub folders and files
                for content in contents:
                    newFolder.addChild(content)

                # Create a vault if necessary
                if toLock: newFolder = encrypt(newFolder, password)

                localContent.append(newFolder)

            elif body.get("type") == "file":
                if toLock:
                    # Create a vault if necessary
                    localContent.append(encrypt(File(name, path, attribs), password))
                else:
                    localContent.append(File(name, path, attribs))
            elif body.get("type") == "vault":
                localContent.append(Vault(name, path, attribs))

    return localContent

def _unloadExplore(object):

    data = {}

    # Determine the type of the object
    if isinstance(object, Folder):
        data["type"] = 'folder'
    elif isinstance(object, File):
        data["type"] = 'file'
    elif isinstance(object, Vault):
        data["type"] = 'vault'

    # Extract the settings of the object
    for attrib in dir(object):

        # Ignore the built-in methods
        if attrib.startswith('_'): continue
        
        # Serialize the children of the object
        if attrib == "children":
            data["files"] = {}
            for childName in object.children:
                childData = _unloadExplore(object.children[childName])
                data["files"][childName] = childData
            continue

        value = getattr(object, attrib)
        if ismethod(value): continue
        data[attrib] = value

    return data
