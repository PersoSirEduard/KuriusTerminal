from types import ClassMethodDescriptorType
import discord
import shlex
from utils import *
from tree import Tree
from folder import *
from file import *
from colors import COLORS
from io import BytesIO

# Bot permissions
intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

TOKEN = 'OTA4NTYzNTMyNDg2OTUwOTEy.YY3jug.9a8bQyIyqS9dxbCpUi2AO-O9F84'
focus_channel = 904198381734330378 # Bot testing channel, we'll change it later
treeDir = Tree()

@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord.')
	treeDir.load("directory.json") # Load the files and folders

@client.event
async def on_message(message):
	
	if message.author == client.user: return # Ignore self messages
	if message.channel.id != focus_channel: return # Only accept messages in the terminal channel
	if message.author.bot: return # Ignore bots to avoid spam

	for command in message.content.split("&&"):
		if command == "": continue
		await handleCommand(message, command)
	

async def handleCommand(message, command):

	args = []
	try:
		args = shlex.split(command) # Split the message into words
	except ValueError as e:
		print(e)

	if args == []: return None # Ignore empty messages/images etc.

	if args[0].startswith('!'): return None # Ignore commands
	
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

			await echo(message.channel, f"Here's a list of most commands: \n{helpTxt}")
			return helpTxt

		# Echo to output
		if args[0] == "echo":
			txt = ' '.join(args[1:])
			await echo(message.channel, txt)
			return txt

		# Echo the current directory
		if args[0] == "pwd":
			await echo(message.channel, treeDir.getCurrentDir())
			return treeDir.getCurrentDir()

		# List current directory files
		if args[0] == "ls": # Only works if the folder contains folders
			try:
				
				folder = treeDir.getDirectory(treeDir.getCurrentDir())

				# Preview sub folders if required
				if "-t" in args:
					await echo(message.channel, f"Found {folder.count} file(s).\n" + treeDir.getTreePath(folder, 3, 0, True, "-f" in args))
				else:
					await echo(message.channel, f"Found {folder.count} file(s).\n" + treeDir.getTreePath(folder, 1, 0, False, "-f" in args))
				
				return [child.getName() for child in folder.children]

			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the directory.", COLORS["red"])
			return None

		# Change directory

		if args[0] == "cd":
			try:
				if (len(args) > 1):
					newPath = args[1]
					
					newDir = treeDir.getDirectory(newPath, True)

					if newDir != None:
						treeDir.setCurrentDir(newDir.getFullPath())
						await echo(message.channel, f"Changed directory to {newDir}.", COLORS["green"])
						return newDir
					else:
						await echo(message.channel, f"Error: Directory not found.", COLORS["red"])
						
				else:
					await echo(message.channel, f"Error: No directory specified.", COLORS["red"])

			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the directory.", COLORS["red"])
			return None

		# Output the contents of a file
		if args[0] == "cat":
			try:
				if (len(args) > 1):
					file = getFile(treeDir, args[1], True)

					if file != None:
						contents = file.read()
						
						if contents != None:
							await echo(message.channel, contents)
							return contents
						else:
							await echo(message.channel, "Error: Could not read the file.", COLORS["red"])
					else:
						await echo(message.channel, f"Error: File not found.", COLORS["red"])

				else:
					await echo(message.channel, f"Error: No file specified.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the file.", COLORS["red"])
			return None

		# Download a file
		if args[0] == "get":
			try:
				if (len(args) > 1):
					file = getFile(treeDir, args[1], True)

					if file != None:
						await message.channel.send(file=discord.File(BytesIO(file.read(mode="rb", limit=False)), filename=file.getName()))
					else:
						await echo(message.channel, f"Error: File not found.", COLORS["red"])
				else:
					await echo(message.channel, f"Error: No file specified.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the file.", COLORS["red"])
			return None
		
		await echo(message.channel, "Unknown command. Use 'help' for all available commands.", COLORS["red"])
		return None

if __name__ == "__main__":
	client.run(TOKEN)