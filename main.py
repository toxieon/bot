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
        'commands.sc_teams',  # Updated with the correct directory name
        'commands.role',
        'commands.exportPFPs',
        'commands.write_contest',
        'commands.timezone',
        'commands.security'  # Add the new security commands here
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

# Custom Thelp command to show all available commands dynamically
@bot.command(name="help")
async def commands_list(ctx):
    """Shows all available commands dynamically."""
    command_list = [command.name for command in bot.commands]
    commands_str = "\n".join([f"• {cmd}" for cmd in command_list])
    await ctx.send(f"Here are all available commands:\n{commands_str}")

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
