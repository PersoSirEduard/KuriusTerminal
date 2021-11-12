import discord

intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

directory = {"Kurius": {"Documents": {"Code": {"Python": {"Bot": {"BotCommands.txt": "commands.txt"} # cmds
                                                            }
                                                }, 
                                    "School": {"Math": {"BigNumber.txt": "bignumber.txt", # Base64
                                                        "RecursiveAlgo.txt": "algorithm.txt"}, # Algorithm
                                                "Web Dev": {"homework.html": "index.html"} # Website
                                                },
                                    "Work": {}
                                        },
                        "Pictures": {"DogPic.png": "dogpic.png", # Steganography
                                    "CatPic.png": "catpic.png", # Steganography
                                    "KuriusLogo.png": "logo.png", 
                                    "Password.png": "password.png"}, # Computer Vision
                        "Downloads": {}}} # Some cryptic files or something


TOKEN = ''

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord.')


@client.event
async def on_message(message):
    global directory

    if message.author == client.user: return # Ignore self messages