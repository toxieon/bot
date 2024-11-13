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

# Automatically load all cogs from the commands directory
for filename in os.listdir('./commands'):
    if filename.endswith('.py') and not filename.startswith('_'):
        bot.load_extension(f'commands.{filename[:-3]}')

# Event triggered when bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    print(f'Bot ID: {bot.user.id}')
    print('------')

# Run bot in a separate thread
TOKEN = os.getenv('discordkey')
if TOKEN:
    threading.Thread(target=bot.run, args=(TOKEN,)).start()
else:
    print("Error: discordkey environment variable is not set.")

# Set up a basic HTTP server to keep the web service alive
class SimpleHTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running")

# Run the HTTP server on the specified port
port = int(os.environ.get("PORT", 8080))
httpd = HTTPServer(("0.0.0.0", port), SimpleHTTPRequestHandler)  # Bind to all interfaces
print(f"Starting HTTP server on port {port}")
httpd.serve_forever()
