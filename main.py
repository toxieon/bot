import discord
from discord.ext import commands
import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler

# Define bot intents
intents = discord.Intents.default()
intents.message_content = True

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
TOKEN = os.getenv('discordkey')
if TOKEN:
    # Start the bot in a separate thread
    threading.Thread(target=bot.run, args=(TOKEN,)).start()
else:
    print("Error: discordkey environment variable is not set.")

# Set up a basic HTTP server to keep the web service alive
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

# Run the HTTP server on the port provided by the platform
port = int(os.environ.get("PORT", 8080))
httpd = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)
print(f"Starting HTTP server on port {port}")
httpd.serve_forever()
