import discord
from flask import Flask, request
from threading import Thread
from functools import partial
import random

# Bot permissions
intents = discord.Intents.default()
intents.presences = True
intents.members = True
client = discord.Client(intents=intents)

app = Flask(__name__)

app_run = partial(app.run, host="0.0.0.0", port=80, debug=True, use_reloader=False)

TOKEN = 'OTE0MDE3MjI2ODc5ODE5Nzc2.YaG64A.GUAjZM8ipMNarx4pOXF0GyJy42U'
SECURITY_KEY = '[tL1O^Up@9bu}&'
BIG_KURIUS_KEY = '7<8/a<6dwc%@`$NU'


user_passwords = ["Wq2A8p", "Bz3mhj", "AtQ4Ns", "Nx7td4", "Lm2hZf", "Yn4fKz", "TuS98q", "Jrb8YB", "Gz4yjg", "Rv24EA"]
blacklist_users = []

@app.route("/new_message", methods=['POST'])
def new_message():
    if not request.headers.get('X-SECURITY-KEY') == SECURITY_KEY: return
    if random.random() <= 0.03:
        with open("random.txt", "r") as file:
            lines = file.readlines()
            selected_line = random.choice(lines)
            userId = request.data.get('user')
            if userId:
                client.get_user(userId).send(selected_line)


@client.event
async def on_ready():
	print(f'{client.user} has connected to Discord.')
	
@client.event
async def on_message(message):
    if message.author == client.user: return # Ignore messages from the bot itself
    if not isinstance(message.channel, discord.channel.DMChannel): return # Only respond to DMs

    if message.content.strip() != BIG_KURIUS_KEY:
        with open("messages.txt", "r") as file:
            lines = file.readlines()
            selected_line = random.choice(lines)
            await message.channel.send(selected_line)
        return
    
    if message.author.id in blacklist_users:
        await message.channel.send("You have way too much greed.")
    else:
        blacklist_users.append(message.author.id)
        if len(user_passwords) > 0:
            password = random.choice(user_passwords)
            user_passwords.remove(password)
            await message.channel.send(f"I won't tell you the whole thing, but here is part of it: {password}")
        else:
            await message.channel.send("I can't give you anything. Ask your comrades.")
        
            
if __name__ == "__main__":
	t = Thread(target=app_run)
	t.start()
	client.run(TOKEN)