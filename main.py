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
        'commands.scteams',
        'commands.role',
        'commands.exportPFPs',
        'commands.write_contest',
        'commands.timezone'
    ]

    for extension in extensions:
        try:
            await bot.load_extension(extension)
            print(f"Successfully loaded: {extension}")
        except Exception as e:
            print(f"Failed to load extension {extension}: {e}")


@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    await load_commands()


# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
