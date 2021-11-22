import json
from colors import COLORS
import discord

def hasPermission(user, requirement : str):
    with open('permissions.json') as file:
        requiredLevels = json.loads(file.read()).get("commands").get(requirement)
        userRoles = [role.name for role in user.roles]
        if requiredLevels != None:
            for level in requiredLevels:
                if level in userRoles: return True
        return False

async def gainPermission(message, permission, password):
    with open('permissions.json') as file:
        requiredLevels = json.loads(file.read()).get("users").get(permission)
        if permission == None: return False

        # Verify the password for the permission
        permPass = requiredLevels.get("password")
        if permPass == None or permPass != password: return False

    # Add permission to the user
    role = discord.utils.get(message.guild.roles, name=permission)
    await message.author.add_roles(role)
    return True

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
