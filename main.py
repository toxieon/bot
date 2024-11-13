import discord
from discord.ext import commands
import os

# Initialize bot with command prefix
bot = commands.Bot(command_prefix='!')

# Load the scores_google_sheets Cog
bot.load_extension("commands.scores_google_sheets")

# Event triggered when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

# Run bot
TOKEN = os.getenv('DISCORD_TOKEN')  # Ensure your token is set as an environment variable
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: DISCORD_TOKEN environment variable is not set.")
