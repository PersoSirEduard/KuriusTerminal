import json
from colors import COLORS

# Send text to the terminal (discord channel)
async def echo(channel, msg, color = COLORS["white"]):
    await channel.send(f"```{color + msg}```")
