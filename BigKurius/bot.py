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

user_passwords = []
blacklist_users = []

@app.route("/new_message", methods=['POST'])
def new_message():
    if not request.headers.get('X-SECURITY-KEY') == SECURITY_KEY: return
    if random.random() < 0.03:
        with open("messages.txt", "r") as file:
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
	if message.author.id in blacklist_users:
		pass
	
if __name__ == "__main__":
	t = Thread(target=app_run)
	t.start()
	client.run(TOKEN)