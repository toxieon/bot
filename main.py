import discord
from discord.ext import commands
import os

# Define bot intents (customize as needed)
intents = discord.Intents.default()
intents.message_content = True  # Enable this if the bot needs to read message content

# Initialize bot with command prefix and intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Load the scores_google_sheets Cog
bot.load_extension("commands.scores_google_sheets")

# Event triggered when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

# Run bot
TOKEN = os.getenv('discordkey')  # Adjusted to match your environment variable
if TOKEN:
    bot.run(TOKEN)
else:
    print("Error: discordkey environment variable is not set.")
