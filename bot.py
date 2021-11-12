import discord
import shlex
import json

intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

TOKEN = ''
treeDir = {}
currentDir = "/"

@client.event
async def on_ready():
	global treeDir
    print(f'{client.user} has connected to Discord.')
	treeDir = loadTreeDir() # Load the files and folders

@client.event
async def on_message(message):
    global treeDir
	global currentDir

    if message.author == client.user: return # Ignore self messages
	
def loadTreeDir():
	try:
		with open('director.json', 'r') as file:
			return json.load(file.read())
	except:
		print("Error: Could not read the tree directory")
		return {}