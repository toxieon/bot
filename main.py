import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Important: Enable this for handling commands

# Initialize the bot and make it case-insensitive
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

# Load commands from external files
async def load_commands():
    extensions = [
        'commands.ping',
        'commands.sc_teams',
        'commands.role',
        'commands.exportPFPs',
        'commands.write_contest',
        'commands.timezone',
        'commands.security',
        'commands.scores',  # Ensure this is the exact filename of scores.py
    ]
    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"Loaded extension: {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_commands()
    try:
        await bot.load_extension('commands.scores')  # Explicitly load scores to catch errors
        print("Scores extension loaded successfully.")
    except Exception as e:
        print(f"Error loading scores extension: {e}")

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
