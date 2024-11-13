import discord
from discord.ext import commands
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Sheets setup
SHEET_ID = '1EUS0M_FK4UbUot8xnKpnDS5nOZGT5YV1IXcyg1kf8bI'
SHEET_NAME = 'Sheet1'  # Change to your sheet's name if different

class ScoreManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheet = self.connect_to_sheet()

    def connect_to_sheet(self):
        # Connect to Google Sheets
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/spreadsheets",
                 "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
        creds = ServiceAccountCredentials.from_json_keyfile_name('path_to_your_credentials.json', scope)
        client = gspread.authorize(creds)
        return client.open_by_key(SHEET_ID).worksheet(SHEET_NAME)

    def get_player_scores(self, player_name):
        # Get player stats (wins/losses)
        records = self.sheet.get_all_records()
        win_count, loss_count = 0, 0
        for row in records:
            if row['Player'] == player_name:
                for key, value in row.items():
                    if value == "V":
                        win_count += 1
                    elif value == "L":
                        loss_count += 1
        return win_count, loss_count

    @commands.command(name="Score")
    async def player_score(self, ctx, player_name: str):
        """Shows overall scores and games won/lost by the player."""
        win_count, loss_count = self.get_player_scores(player_name)
        await ctx.send(f"{player_name} has {win_count} wins and {loss_count} losses.")

    @commands.command(name="Players")
    async def list_players(self, ctx):
        """Lists all players."""
        players = [self.sheet.cell(row, 1).value for row in range(2, len(self.sheet.get_all_records()) + 2)]
        await ctx.send("Players: " + ", ".join(players))

    @commands.command(name="ScoreUpdate")
    async def score_update(self, ctx, player1: str, player2: str, winner: int):
        """Updates the sheet based on the winner of a match."""
        row1 = self.sheet.find(player1).row
        col2 = self.sheet.find(player2).col
        if winner == 1:
            self.sheet.update_cell(row1, col2, "V")
            self.sheet.update_cell(col2, row1, "L")
        elif winner == 2:
            self.sheet.update_cell(row1, col2, "L")
            self.sheet.update_cell(col2, row1, "V")
        await ctx.send(f"Score updated: {player1} vs {player2}.")

    @commands.command(name="Upcoming")
    async def upcoming_matches(self, ctx, player_name: str = None):
        """Shows all games yet to be played, or for a specific player."""
        rows = self.sheet.get_all_records()
        upcoming = []
        for row in rows:
            for col, value in row.items():
                if value == "":
                    match = f"{row['Player']} vs {col}"
                    if not player_name or player_name in match:
                        upcoming.append(match)
        await ctx.send("Upcoming matches:\n" + "\n".join(upcoming))

async def setup(bot):
    await bot.add_cog(ScoreManager(bot))
