from types import ClassMethodDescriptorType
import discord
import shlex
from utils import *
from tree import Tree
from folder import *
from file import *
from colors import COLORS

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

	# # Split the message into words
	args = shlex.split(message.content)

	if args[0].startswith('!'): return # Ignore commands
	
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
			return

		# Echo to output
		if args[0] == "echo":
			await echo(message.channel, f"{' '.join(args[1:])}")
			return

		# Echo the current directory
		if args[0] == "pwd":
			await echo(message.channel, treeDir.getCurrentDir())
			return

		# List current directory files
		if args[0] == "ls": # Only works if the folder contains folders
			try:
				folder = treeDir.getDirectory(treeDir.getCurrentDir())

				# Previw sub folders if required
				if "-s" in args:
					await echo(message.channel, f"Found {folder.count} file(s).\n" + treeDir.getTreePath(folder, 3, 0, True))
				else:
					await echo(message.channel, f"Found {folder.count} file(s).\n" + treeDir.getTreePath(folder, 1, 0, False))
				
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the directory.", COLORS["red"])
			return

		# Change directory

		if args[0] == "cd":
			try:
				if (len(args) > 1):
					newPath = args[1]

					if newPath.startswith(".."):
						newPath = str(treeDir.getDirectory(treeDir.getCurrentDir())) + newPath[2:]
					elif newPath.startswith('~'):
						newPath = '/' + newPath[1:]
					elif newPath.startswith('.'):
						newPath = treeDir.getCurrentDir() + '/' + newPath[1:]
					else:
						newPath = treeDir.getCurrentDir() + "/" + newPath

					newDir = treeDir.getDirectory(newPath)

					if newDir != None:
						treeDir.setCurrentDir(newPath)
						await echo(message.channel, f"Changed directory to {newPath}.", COLORS["green"])
					else:
						await echo(message.channel, f"Error: Directory not found.", COLORS["red"])
						
				else:
					await echo(message.channel, f"Error: No directory specified.", COLORS["red"])

			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the directory.", COLORS["red"])
			return
		
		await echo(message.channel, "Unknown command. Use 'help' for all available commands.", COLORS["red"])

if __name__ == "__main__":
	client.run(TOKEN)