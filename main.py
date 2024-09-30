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

# Lock system to restrict commands and manage security levels
locked_commands = {}  # Format: {command_name: level (1-5)}
user_security_levels = {}  # Format: {username: security_level (1-5)}

# Load locked commands and security levels from JSON files
LOCKED_COMMANDS_FILE = "locked_commands.json"
SECURITY_LEVELS_FILE = "security_levels.json"


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


def load_security_levels():
    global user_security_levels
    if os.path.exists(SECURITY_LEVELS_FILE):
        with open(SECURITY_LEVELS_FILE, 'r') as file:
            user_security_levels = json.load(file)
    else:
        user_security_levels = {}


def save_security_levels():
    with open(SECURITY_LEVELS_FILE, 'w') as file:
        json.dump(user_security_levels, file)


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
    load_security_levels()
    await load_commands()

# Lock and unlock commands for bot owner with multiple command support and security levels
@bot.command(name="lock")
@commands.is_owner()
async def lock(ctx, *, commands_with_levels: str):
    """Locks commands with an optional security level."""
    commands_with_levels = commands_with_levels.split(',')
    for item in commands_with_levels:
        parts = item.strip().split()
        command_name = parts[0]
        level = int(parts[1]) if len(parts) > 1 else 5  # Default to level 5 if no level is provided
        if command_name in bot.all_commands:
            locked_commands[command_name] = level
            await ctx.send(f"The command `{command_name}` is now locked with security level {level}.")
        else:
            await ctx.send(f"Command `{command_name}` not found.")
    save_locked_commands()


@bot.command(name="unlock")
@commands.is_owner()
async def unlock(ctx, *, command_names: str):
    """Unlocks multiple commands."""
    command_names = command_names.split(',')
    for command_name in command_names:
        command_name = command_name.strip()
        if command_name in locked_commands:
            locked_commands.pop(command_name, None)
            await ctx.send(f"The command `{command_name}` is now unlocked.")
        else:
            await ctx.send(f"Command `{command_name}` is not locked.")
    save_locked_commands()


# Command to set security levels for users
@bot.command(name="security")
@commands.is_owner()
async def set_security(ctx, level: int, *, player: str):
    """Sets the security level for a player (only accessible by bot owner)."""
    member = discord.utils.get(ctx.guild.members, name=player)
    if member:
        user_security_levels[member.name] = level
        save_security_levels()
        await ctx.send(f"Security level {level} has been set for {member.name}.")
    else:
        await ctx.send(f"User `{player}` not found.")


# Show all currently locked commands
@bot.command(name="locked")
async def show_locked(ctx):
    """Displays all locked commands."""
    if locked_commands:
        locked_list = "\n".join([f"• {cmd} (Level {level})" for cmd, level in locked_commands.items()])
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
    """Global check to block locked commands for users without the appropriate security level."""
    if ctx.command and ctx.command.name in locked_commands:
        user_level = user_security_levels.get(ctx.author.name, 5)  # Default security level is 5 (lowest)
        required_level = locked_commands[ctx.command.name]
        if user_level <= required_level:
            return True
        else:
            await ctx.send(f"You do not have the required security level to use `{ctx.command}` (Level {required_level}).")
            return False
    return True

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
