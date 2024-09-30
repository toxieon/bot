import discord
from discord.ext import commands
import os
import webserver
import json

DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Important: Enable this for handling commands

# Initialize the bot and make it case-insensitive
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

# Lock system to restrict commands
locked_commands = {}

# Load locked commands from a JSON file
LOCKED_COMMANDS_FILE = "locked_commands.json"


def load_locked_commands():
    global locked_commands
    if os.path.exists(LOCKED_COMMANDS_FILE):
        with open(LOCKED_COMMANDS_FILE, 'r') as file:
            locked_commands = json.load(file)
    else:
        locked_commands = {}


def save_locked_commands():
    with open(LOCKED_COMMANDS_FILE, 'w') as file:
        json.dump(locked_commands, file)


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
    load_locked_commands()
    await load_commands()

# Lock and unlock commands for bot owner
@bot.command(name="lock")
@commands.is_owner()
async def lock(ctx, command_name: str):
    """Locks a command so only the owner can use it."""
    if command_name in bot.all_commands:
        locked_commands[command_name] = True
        save_locked_commands()
        await ctx.send(f"The command `{command_name}` is now locked for general use.")
    else:
        await ctx.send(f"Command `{command_name}` not found.")


@bot.command(name="unlock")
@commands.is_owner()
async def unlock(ctx, command_name: str):
    """Unlocks a command for general use."""
    if command_name in locked_commands:
        locked_commands.pop(command_name, None)
        save_locked_commands()
        await ctx.send(f"The command `{command_name}` is now unlocked for general use.")
    else:
        await ctx.send(f"Command `{command_name}` is not locked.")


# Show all currently locked commands
@bot.command(name="locked")
async def show_locked(ctx):
    """Displays all locked commands."""
    if locked_commands:
        locked_list = "\n".join([f"• {cmd}" for cmd in locked_commands])
        await ctx.send(f"The following commands are currently locked:\n{locked_list}")
    else:
        await ctx.send("There are no locked commands.")


# Show all currently unlocked commands
@bot.command(name="unlocked")
async def show_unlocked(ctx):
    """Displays all unlocked commands."""
    all_commands = set(bot.all_commands)
    locked_set = set(locked_commands)
    unlocked_commands = all_commands - locked_set

    if unlocked_commands:
        unlocked_list = "\n".join([f"• {cmd}" for cmd in unlocked_commands])
        await ctx.send(f"The following commands are currently unlocked:\n{unlocked_list}")
    else:
        await ctx.send("All commands are currently locked.")


@bot.check
async def globally_block_locked_commands(ctx):
    """Global check to block locked commands for non-owners."""
    if ctx.command and ctx.command.name in locked_commands:
        if await bot.is_owner(ctx.author):
            return True
        else:
            await ctx.send(f"The command `{ctx.command}` is currently locked and cannot be used.")
            return False
    return True

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
