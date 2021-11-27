import discord
import shlex
from utils import *
from tree import Tree
from folder import *
from file import *
from vault import encrypt
from colors import COLORS
from io import BytesIO

# Bot permissions
intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

TOKEN = 'OTA4NTYzNTMyNDg2OTUwOTEy.YY3jug.9a8bQyIyqS9dxbCpUi2AO-O9F84'
focus_channel = 913947810485927956 # Bot testing channel, we'll change it later
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

	for command in message.content.split("&&")[:3]:
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

	for a in range(len(args)): args[a] = treeDir.env.applyVars(args[a]) # Apply environment variables
	
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
				
				folder = treeDir.getDirectory(treeDir.getCurrentDir(), user=message.author)

				# Preview sub folders if required
				if "-t" in args:
					await echo(message.channel, f"Found {folder.count} file(s).\n" + treeDir.getTreePath(folder, 3, 0, True, "-f" in args))
				else:
					await echo(message.channel, f"Found {folder.count} file(s).\n" + treeDir.getTreePath(folder, 1, 0, False, "-f" in args))
				
				return folder.children.keys()

			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the directory.", COLORS["red"])
			return None

		# Change directory

		if args[0] == "cd":
			try:
				if (len(args) > 1):
					newPath = args[1]
					
					newDir = treeDir.getDirectory(newPath, True, user=message.author)

					if newDir != None:
						treeDir.setCurrentDir(newDir.getFullPath())
						await echo(message.channel, f"Changed directory to {newDir}.", COLORS["green"])
						return newDir

					else:
						await echo(message.channel, f"Error: Directory not found or user permission required.", COLORS["red"])
						
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
					file = getFile(treeDir, args[1], True, message.author)

					if file != None:
						contents = file.read()
						
						if contents != None:
							await echo(message.channel, contents)
							return contents
						else:
							await echo(message.channel, "Error: Could not read the file.", COLORS["red"])
					else:
						await echo(message.channel, f"Error: File not found or user permission required.", COLORS["red"])

				else:
					await echo(message.channel, f"Error: No file specified.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the file.", COLORS["red"])
			return None

		# Download a file
		if args[0] == "grab":
			try:
				if (len(args) > 1):
					file = getFile(treeDir, args[1], True, message.author)

					if file != None:
						await message.channel.send(file=discord.File(BytesIO(file.read(mode="rb", limit=False)), filename=file.getName()))
					else:
						await echo(message.channel, f"Error: File not found or user permission required.", COLORS["red"])
				else:
					await echo(message.channel, f"Error: No file specified.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not reach the contents of the file.", COLORS["red"])
			return None

		# Add/Change user permission level
		if args[0] == "su":
			try:
				if (len(args) > 2):
					permission = args[1]
					password = args[2]

					if await gainPermission(message, permission, password):
						await echo(message.channel, f"Gained {permission} privileges.", COLORS["green"])
					else:
						await echo(message.channel, f"Error: Could not gain permssion. Verify your password.", COLORS["red"])

				else:
					await echo(message.channel, f"Error: Invalid input. A permission name and a password are required.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Something went wrong.", COLORS["red"])
			return None
		
		# Unlock a vault
		if args[0] == "unlock":
			try:
				if (len(args) > 2):

					# if not hasPermission(message.author, "unlock"):
						# await echo(message.channel, f"Error: You do not have permission to unlock.", COLORS["red"])
						# return None

					file = getFile(treeDir, args[1], True, user=message.author)

					if file != None:
						unlocked = file.decrypt(args[2])
						treeDir.getDirectory(file.getParentPath(), user=message.author).children[file.getName()] = unlocked
						await echo(message.channel, f"Unlocked {file.getName()}.", COLORS["green"])
						return unlocked
					else:
						await echo(message.channel, f"Error: File not found or user permission required.", COLORS["red"])
				else:
					await echo(message.channel, f"Error: No file or password specified.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not unlock. The password may be invalid.", COLORS["red"])
			return None

		# Create a vault
		if args[0] == "lock":
			try:
				if (len(args) > 2):

					if not hasPermission(message.author, "lock"):
						await echo(message.channel, "Error: You do not have permission to lock files.", COLORS["red"])
						return None
					
					objet = None

					try:
						object = getFile(treeDir, args[1], True, user=message.author)
					except:
						object = None
					
					try:
						object = getDirectory(treeDir, args[1], True, user=message.author)
					except:
						object = None

					if object != None:
						locked = encrypt(object, args[2])
						treeDir.getDirectory(object.getParentPath(), user=message.author).children[object.getName()] = locked
						treeDir.setCurrentDir(object.getParentPath())

						await echo(message.channel, f"Locked {locked.getName()}.", COLORS["green"])
						return locked
					else:
						await echo(message.channel, f"Error: Invalid folder or file.", COLORS["red"])
				else:
					await echo(message.channel, f"Error: No file/folder or password specified.", COLORS["red"])

			except Exception as e:
				print(e)
				await echo(message.channel, "Error: Could not lock.", COLORS["red"])
			return None

		# Neofetch show system information
		if args[0] == "neofetch":
			with open("neofetch.txt", "r") as f:
				await echo(message.channel, treeDir.env.applyVars(f.read()), COLORS["blue"])
			return None

		# Get system variable
		if args[0] == "get":
			try:
				if "-a" in args: # Get all variables
					vars = treeDir.env.getAllVars()
					await echo(message.channel, '\n'.join([i + " = " + vars[i] for i in vars]))
					return args[1]
				
				if len(args) > 1:
					var = treeDir.env.get(args[1])

					if var != None:
						await echo(message.channel, var)
						return var
					else:
						await echo(message.channel, f"Error: Variable not found.", COLORS["red"])
					
				else:
					await echo(message.channel, f"Error: Missing the variable's name.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, f"Error: Could not get \"{args[1]}\".", COLORS["red"])
			return None
		
		# Set system variable
		if args[0] == "set":
			try:
				if len(args) > 2:
					treeDir.env.set(args[1], args[2])
					await echo(message.channel, f"Set \"{args[1]}\" to \"{args[2]}\"")
					return args[2]
				else:
					await echo(message.channel, f"Error: Missing the variable's name or/and value.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, f"Error: Could not set \"{args[1]}\".", COLORS["red"])
			return None

		# Delete system variable
		if args[0] == "del":
			try:
				if len(args) > 1:
					if treeDir.env.delete(args[1]):
						await echo(message.channel, f"Deleted \"{args[1]}\".")
						return args[1]
					else:
						await echo(message.channel, f"Error: Variable not found or cannot be removed.", COLORS["red"])
						return None
				else:
					await echo(message.channel, f"Error: Missing the variable's name.", COLORS["red"])
			except Exception as e:
				print(e)
				await echo(message.channel, f"Error: Could not delete \"{args[1]}\".", COLORS["red"])
			return None

		await echo(message.channel, "Unknown command. Use 'help' for all available commands.", COLORS["red"])
		return None

if __name__ == "__main__":
	client.run(TOKEN)
