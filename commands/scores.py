import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Setup Google Sheets API scope and credentials
SHEET_SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
               "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

# Replace 'SussyBaka.json' with the name of your credentials file
CREDS_FILE = "SussyBaka.json"
SHEET_NAME = "Prelim Round Robin"

# Authenticate and access the sheet
creds = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SHEET_SCOPE)
client = gspread.authorize(creds)
sheet = client.open(SHEET_NAME).sheet1


class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Players")
    async def list_players(self, ctx):
        """List all players in the tournament."""
        players = sheet.col_values(1)[1:]  # Get all player names in the first column, excluding the header
        player_list = "\n".join(players)
        await ctx.send(f"Players in the tournament:\n{player_list}")

    @commands.command(name="Score")
    async def get_score(self, ctx, player_name: str):
        """Retrieve the win/loss record for a specific player."""
        players = sheet.col_values(1)
        if player_name not in players:
            await ctx.send(f"Player '{player_name}' not found.")
            return

        player_row = players.index(player_name) + 1
        results = sheet.row_values(player_row)[1:]
        wins = results.count("V")
        losses = results.count("L")

        await ctx.send(f"{player_name} - Wins: {wins}, Losses: {losses}")

    @commands.command(name="Score_Update")
    async def update_score(self, ctx, player1: str, player2: str, winner: int):
        """Update the score between two players."""
        players = sheet.col_values(1)

        if player1 not in players or player2 not in players:
            await ctx.send("One or both players not found in the sheet.")
            return

        player1_row = players.index(player1) + 1
        player2_row = players.index(player2) + 1
        player1_col = sheet.row_values(1).index(player1) + 1
        player2_col = sheet.row_values(1).index(player2) + 1

        if winner == 1:
            sheet.update_cell(player1_row, player2_col, "V")
            sheet.update_cell(player2_row, player1_col, "L")
            await ctx.send(f"{player1} is recorded as the winner against {player2}.")
        elif winner == 2:
            sheet.update_cell(player1_row, player2_col, "L")
            sheet.update_cell(player2_row, player1_col, "V")
            await ctx.send(f"{player2} is recorded as the winner against {player1}.")
        else:
            await ctx.send("Invalid winner specified. Use 1 for player1 or 2 for player2.")

    @commands.command(name="upcoming")
    async def upcoming_matches(self, ctx, player_name: str = None):
        """List upcoming matches, or upcoming matches for a specific player if provided."""
        players = sheet.col_values(1)[1:]  # Get all players except the header
        all_matches = []

        if player_name:
            if player_name not in players:
                await ctx.send(f"Player '{player_name}' not found.")
                return

            player_row = players.index(player_name) + 2
            for col, opponent in enumerate(players, start=2):
                if sheet.cell(player_row, col).value == "":
                    all_matches.append(opponent)

            match_list = "\n".join(all_matches)
            await ctx.send(f"Upcoming matches for {player_name}:\n{match_list}")

        else:
            for i, player in enumerate(players, start=2):
                for j, opponent in enumerate(players, start=2):
                    if i != j and sheet.cell(i, j).value == "":
                        all_matches.append(f"{player} vs {opponent}")

            match_list = "\n".join(all_matches)
            await ctx.send(f"All upcoming matches:\n{match_list}")


# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(Scores(bot))
