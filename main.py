import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()
intents.members = True  # Enable member intent (if needed)
intents.message_content = True  # Important: Enable this for handling commands like !Ping, !Role

bot = commands.Bot(command_prefix='!', intents=intents)

# Print the bot's status when it's ready
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

# Simple ping command
@bot.command(name="Ping")
async def ping(ctx):
    print("Ping command received!")
    await ctx.send("ToxiBot Online")

# Role creation command
@bot.command(name="Role")
async def create_role(ctx):
    print("Role command received!")
    await ctx.send("What would you like the Role name to be?")

    role_name_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    role_name = role_name_msg.content.strip()

    await ctx.send(f"What color would you like {role_name} to be?")
    role_color_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    role_color_input = role_color_msg.content.strip().lower()

    print(f"Role name: {role_name}, Color: {role_color_input}")

# Keep bot alive
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
