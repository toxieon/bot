import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Important: Enable this for handling commands

# Initialize the bot
bot = commands.Bot(command_prefix='!', intents=intents)

# Load commands from external files
async def load_commands():
    await bot.load_extension('commands.ping')
    await bot.load_extension('commands.role')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_commands()

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
