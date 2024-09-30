import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ.get('discordkey')
GAME_NAME = os.environ.get('discordgame', 'StarCraft')  # Set a default game name

# Configure bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Important: Enable this for handling commands

# Initialize the bot and make it case-insensitive
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

# Load commands from external files
async def load_commands():
    await bot.load_extension('commands.ping')
    await bot.load_extension('commands.role')
    await bot.load_extension('commands.exportPFPs')
    await bot.load_extension('commands.write_contest')
    await bot.load_extension('commands.timezone')
    await bot.load_extension('commands.sc_teams')
    await bot.load_extension('commands.voice_who')

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

    # Set the bot's game-playing activity
    game = discord.Game(GAME_NAME)  # Use the game from the environment variable
    await bot.change_presence(activity=game)  # Update the bot's status to "Playing {GAME_NAME}"

    await load_commands()

# Custom Thelp command to show all available commands dynamically
@bot.command(name="Thelp")  # Only respond to !Thelp
async def commands_list(ctx):
    """Shows all available commands dynamically."""
    command_list = [command.name for command in bot.commands]
    commands_str = "\n".join([f"• {cmd}" for cmd in command_list])
    await ctx.send(f"Here are all available commands:\n{commands_str}")

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
