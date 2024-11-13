import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define Google Sheets access
SCOPE = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]
CREDS_FILE = "SussyBaka.json"  # Ensure this is the exact file name on GitHub and in your deployment
SHEET_NAME = "Prelim Round Robin"

# Authenticate and access the sheet
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
client = gspread.authorize(credentials)
sheet = client.open(SHEET_NAME).sheet1


class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Players")
    async def list_players(self, ctx):
        """List all players in the tournament."""
        players = sheet.col_values(1)[1:]  # Skip header
        await ctx.send("Players:\n" + "\n".join(players))

    @commands.command(name="Score")
    async def get_score(self, ctx, player: str):
        """Show overall scores and games won/lost by the player."""
        players = sheet.col_values(1)[1:]
        if player not in players:
            await ctx.send(f"{player} is not in the player list.")
            return

        player_row = players.index(player) + 2  # Adjust for 1-indexed and header
        row_values = sheet.row_values(player_row)[1:]  # Skip player name column
        wins = row_values.count("V")
        losses = row_values.count("L")

        await ctx.send(f"{player} has {wins} wins and {losses} losses.")

    @commands.command(name="Score_Update")
    async def update_score(self, ctx, player1: str, player2: str, winner: int):
        """Update score between two players (1 for player1 wins, 2 for player2 wins)."""
        players = sheet.col_values(1)[1:]
        if player1 not in players or player2 not in players:
            await ctx.send("Both players must be in the list.")
            return

        player1_row = players.index(player1) + 2
        player2_row = players.index(player2) + 2
        player1_col = player2_row
        player2_col = player1_row

        if winner == 1:
            sheet.update_cell(player1_row, player1_col, "V")
            sheet.update_cell(player2_row, player2_col, "L")
            await ctx.send(f"{player1} wins against {player2}")
        elif winner == 2:
            sheet.update_cell(player1_row, player1_col, "L")
            sheet.update_cell(player2_row, player2_col, "V")
            await ctx.send(f"{player2} wins against {player1}")
        else:
            await ctx.send("Invalid winner value. Use 1 for player1 or 2 for player2.")

    @commands.command(name="upcoming")
    async def upcoming_matches(self, ctx, player: str = None):
        """List all upcoming matches or those of a specific player."""
        players = sheet.col_values(1)[1:]
        upcoming_matches = []

        if player and player not in players:
            await ctx.send(f"{player} is not in the player list.")
            return

        for i, row_player in enumerate(players):
            row = sheet.row_values(i + 2)[1:]
            for j, cell in enumerate(row):
                if cell == "":
                    opponent = players[j]
                    if not player or player == row_player or player == opponent:
                        upcoming_matches.append(f"{row_player} vs {opponent}")

        if upcoming_matches:
            await ctx.send("Upcoming Matches:\n" + "\n".join(upcoming_matches))
        else:
            await ctx.send("No upcoming matches.")


# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(Scores(bot))
