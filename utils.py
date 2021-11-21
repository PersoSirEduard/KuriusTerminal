import json
from colors import COLORS

def hasPermission(user):
    with open('permissions.json') as file:
        permissions = json.loads(file.read())
        for permission in permissions:
            if permissions[permission][0] in [role.name for role in user.roles ]:
                return True
    return False

# Send text to the terminal (discord channel)
async def echo(channel, msg, color = COLORS["white"]):
    await channel.send(f"```{color + msg}```")

# Support for path link parsing and formatting
def formatPath(treeDir, path):
    if ".." in path: # Go back a directory
						
        currPath = treeDir.getCurrentDir()
        for cdStep in path.split("/"):
            if cdStep == "..":
                parentDir = (treeDir.getDirectory(currPath)).getParentPath()
                currPath = parentDir
            elif cdStep != "":
                currPath += "/" + cdStep
        
        return currPath

    elif path.startswith('~'):
        return '/' + path[1:]
    elif path.startswith('.'):
        return treeDir.getCurrentDir() + '/' + path[1:]
    else:
        return treeDir.getCurrentDir() + '/' + path
