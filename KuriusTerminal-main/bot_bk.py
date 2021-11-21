import discord
import shlex
from utils import *

# Bot permissions
intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

TOKEN = 'OTA4NTYzNTMyNDg2OTUwOTEy.YY3jug.9a8bQyIyqS9dxbCpUi2AO-O9F84'
focus_channel = 904198381734330378 # Bot testing channel, we'll change it later
treeDir = {}
currentDir = "/"

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord.')
	global treeDir
	treeDir = loadTreeDir() # Load the files and folders

@client.event
async def on_message(message):
	global currentDir, treeDir
	
	if message.author == client.user: return # Ignore self messages
	if message.channel.id != focus_channel: return # Only accept messages in the terminal channel

	# Split the message into words
	args = shlex.split(message.content)
	
	async with message.channel.typing(): # Show that the bot is computing

		# Help message
		if args[0] == "help":

			# Load help text
			with open('help.json', 'r') as file:
				commands = json.loads(file.read())

			helpTxt = ""
			for cmd in commands:
				helpTxt += f"{cmd}: {commands[cmd]}\n"
			helpTxt += "Please report any issue to a Community Manager."

			await message.channel.send(f"```Here's a list of most commands: \n{helpTxt}```")
			return

		# Echo to output
		if args[0] == "echo":
			await message.channel.send(f"```{' '.join(args[1:])}```")
			return

		# List current directory files
		if args[0] == "ls": # Only works if the folder contains folders
			folder = getFolderContents(currentDir)
			nl = '\n'
			if folder["success"]:
				await message.channel.send(f"```{folder.get('message') + nl + currentDir + nl + nl.join(drawContents(folder.get('contents')))}```")
			else:
				await message.channel.send(f"```{folder['message']}```")
			return

		# Change directory
		if args[0] == "cd":
			if (len(args) > 1): # Directory argument
				newPath = args[1]

				if newPath.startswith(".."):
					newPath = getParentFolderPath(currentDir) + newPath[2:]
				elif newPath.startswith('~'):
					newPath = '/' + newPath[1:]
				elif newPath.startswith('.'):
					newPath = currentDir + '/' + newPath[1:]
				else:
					newPath = currentDir + "/" + newPath

				if isFolder(newPath):
					currentDir = newPath
					await message.channel.send(f"```Changed directory to {currentDir}.```")
				else:
					await message.channel.send("```Invalid directory.```")

			else:
				await message.channel.send("```Please specify a directory.```")
			return
		
		await message.channel.send("```Unknown command. Use 'help' for all available commands.```")
    
    # if message.content.lower().startswith("cd"):
    #     splitMsg = message.content.split(" ")
    #     if len(splitMsg) < 2: # User only wrote "cd", might need to check for "cd " idk if it causes errors
    #         await message.channel.send("`Error: Expected a directory as argument`")
    #         return
    #     if splitMsg[1] not in currentDir.keys(): # Argument not in directory
    #         await message.channel.send(f"`Error: Could not find '{splitMsg[1]}' in current directory.`")
    #         return
    #     if "." in splitMsg[1]: # Argument is a file, make sure not to put points in folder names
    #         await message.channel.send("`Error: Expected a directory but got a file as argument.`")
    #         return
        
        # currentDir = currentDir[splitMsg[1]]

        # Still have to implement "cd .." to go back a directory

def isFolder(path):
	global treeDir
	pathRoute = [ p for p in path.split("/") if p.strip() != "" ]

	try:
		currFolder = treeDir.get("Kurius")
		for p in pathRoute:
			currFolder = currFolder.get("files", {}).get(p, {})
			if currFolder.get("type") != "folder":
				return False
	except Exception as e:
		print(e)
		return False

	return currFolder


def getFolderContents(path):
	try:
		currFolder = isFolder(path)
		return {
			"success": currFolder != False,
			"message": f"Found {len(currFolder.get('files').keys())} file(s)." if currFolder != False else "Could not reach the contents of the folder",
			"contents": currFolder.get("files") if currFolder != False else {}
		}
	except:
		return {
			"success": False,
			"message": "Could not reach the contents of the folder",
			"contents": {}
		}

def getParentFolderPath(path):
	pathRoute = [ p for p in path.split("/") if p.strip() != "" ]
	if len(pathRoute) == 0:
		return "/"
	elif len(pathRoute) == 1:
		return "/"
	else:
		return "/".join(pathRoute[:-1])

def drawContents(contents):
	result = []
	keys = list(contents.keys()) # List of items in the folder

	# Draw the tree
	for i in range(len(keys)):
		if (i == len(keys) - 1):
			result.append("└ " + keys[i] + ("/" if contents[keys[i]].get("type") == "folder" else ""))
		else:
			result.append("├ " + keys[i] + ("/" if contents[keys[i]].get("type") == "folder" else ""))

	return result

if __name__ == "__main__":
	client.run(TOKEN)