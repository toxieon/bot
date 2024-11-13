import discord
from discord.ext import commands
import gspread
from google.oauth2.service_account import Credentials
import os

# Path to the Google service account JSON file
GOOGLE_SHEET_ID = '1EUS0M_FK4UbUot8xnKpnDS5nOZGT5YV1IXcyg1kf8bI'
SERVICE_ACCOUNT_FILE = 'SussyBaka.json'

# Initialize Google Sheets API credentials
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)
sheet = client.open_by_key(GOOGLE_SHEET_ID).worksheet('Prelim Round Robin')

class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Basic test command to verify that scores.py is working
    @commands.command(name="test_scores")
    async def test_scores(self, ctx):
        await ctx.send("Scores cog is working and loaded!")

    # Example command: !Players
    @commands.command(name="Players")
    async def players_command(self, ctx):
        player_names = sheet.col_values(1)  # Assume player names are in the first column
        await ctx.send(f"Players:\n" + "\n".join(player_names))

    # Example command: !Score (player name)
    @commands.command(name="Score")
    async def score_command(self, ctx, player_name: str):
        # Simplified placeholder: respond with player's score details
        await ctx.send(f"Showing score details for {player_name}")

    # Other commands (upcoming, score_update) follow similar format...

async def setup(bot):
    await bot.add_cog(Scores(bot))
    print("Scores cog loaded successfully.")
