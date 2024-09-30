import discord
from discord.ext import commands
import os
import json
import webserver
from datetime import datetime

DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Important: Enable this for handling commands

# Initialize the bot and make it case-insensitive
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)

# File to store locked commands
LOCKED_COMMANDS_FILE = "locked_commands.json"

# Dictionary to track locked commands
locked_commands = {}

# Load locked commands from file
def load_locked_commands():
    global locked_commands
    if os.path.exists(LOCKED_COMMANDS_FILE):
        with open(LOCKED_COMMANDS_FILE, 'r') as file:
            locked_commands = json.load(file)

# Save locked commands to file
def save_locked_commands():
    with open(LOCKED_COMMANDS_FILE, 'w') as file:
        json.dump(locked_commands, file)

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
    load_locked_commands()  # Load locked commands on startup
    await load_commands()

# Ping command with latency check and dynamic status change
@bot.command(name="ping")
async def ping(ctx):
    """Check the bot's latency and display it."""
    game = discord.Game("Pinging...")
    await bot.change_presence(activity=game)  # Change bot status while processing ping
    latency = round(bot.latency * 1000)  # Convert to milliseconds
    await ctx.send(f"ToxiBot Online! Latency: {latency} ms")
    await bot.change_presence(activity=discord.Game(os.environ.get('discordgame', 'StarCraft')))

# Lock a command (owner-only)
@bot.command(name="lock")
@commands.is_owner()
async def lock(ctx, command_name: str):
    """Locks a command so only the owner can use it."""
    if command_name in bot.all_commands:
        locked_commands[command_name] = True
        save_locked_commands()  # Save the locked state
        await ctx.send(f"The `{command_name}` command has been locked.")
    else:
        await ctx.send(f"No such command `{command_name}` found.")

# Unlock a command (owner-only)
@bot.command(name="unlock")
@commands.is_owner()
async def unlock(ctx, command_name: str):
    """Unlocks a command for general use."""
    if command_name in bot.all_commands:
        if command_name in locked_commands:
            del locked_commands[command_name]
            save_locked_commands()  # Save the unlocked state
            await ctx.send(f"The `{command_name}` command has been unlocked.")
        else:
            await ctx.send(f"The `{command_name}` command is not locked.")
    else:
        await ctx.send(f"No such command `{command_name}` found.")

# Reload a specific command (owner-only)
@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx, extension: str):
    """Reload a specific command or cog."""
    try:
        await bot.reload_extension(f'commands.{extension}')
        await ctx.send(f"Reloaded `{extension}` successfully!")
    except Exception as e:
        await ctx.send(f"Failed to reload `{extension}`: {str(e)}")

# Short command aliases (for frequently used commands)
bot.command(name="role", aliases=["r"])(lock)  # Alias for Role
bot.command(name="SetTimezone", aliases=["tz"])(unlock)  # Alias for SetTimezone

# Dynamic help command
@bot.command(name="Thelp")
async def commands_list(ctx):
    """Shows all available commands dynamically with their descriptions."""
    command_list = [f"• {command.name}: {command.help or 'No description'}" for command in bot.commands if command.name not in locked_commands]
    commands_str = "\n".join(command_list)
    await ctx.send(f"Here are all available commands:\n{commands_str}")

# Command to view the bot's logs (owner-only)
@bot.command(name="logs")
@commands.is_owner()
async def logs(ctx):
    """Fetch and send the bot's latest log output (for admins)."""
    log_file = "bot.log"  # Assuming the bot logs to bot.log
    if os.path.exists(log_file):
        with open(log_file, 'r') as log_file:
            logs = log_file.read()[-2000:]  # Send the last 2000 characters of the log
            await ctx.send(f"```\n{logs}\n```")
    else:
        await ctx.send("Log file not found.")

# Check for locked commands when invoked
@bot.event
async def on_command(ctx):
    command_name = ctx.command.name
    if command_name in locked_commands:
        if not await bot.is_owner(ctx.author):
            await ctx.send(f"The `{command_name}` command is locked and can only be used by the bot owner.")
            return
    await bot.process_commands(ctx)  # Continue processing the command if not locked or if the owner

# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
