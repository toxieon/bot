import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')  # Ensure this is set in the environment
intents = discord.Intents.default()
intents.members = True
intents.message_content = True

# Initialize the bot
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
        'commands.scores',
        'commands.google_sheets'
    ]

    for extension in extensions:
        try:
            await bot.load_extension(extension)
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
