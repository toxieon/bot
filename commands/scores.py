import discord
from discord.ext import commands
from google_sheets import read_sheet, update_sheet

SHEET_ID = '1EUS0M_FK4UbUot8xnKpnDS5nOZGT5YV1IXcyg1kf8bI'
SHEET_NAME = 'Prelim Round Robin'

class ScoreUpdater(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Score_Update")
    async def score_update(self, ctx, player1: str, player2: str, winner: int):
        """Updates the Google Sheet with the result of a game."""
        if winner not in (1, 2):
            await ctx.send("Invalid winner input. Use 1 for the first player or 2 for the second player.")
            return

        data = read_sheet(SHEET_ID, f'{SHEET_NAME}!A1:Z100')
        player1_row, player2_col = None, None

        for i, row in enumerate(data):
            if row[0] == player1:
                player1_row = i + 1
            if row[0] == player2:
                player2_col = i + 1
            if player1_row and player2_col:
                break

        if player1_row is None or player2_col is None:
            await ctx.send("One or both players not found.")
            return

        result = "V" if winner == 1 else "L"
        cell_range = f'{SHEET_NAME}!{chr(64 + player2_col)}{player1_row}'
        update_sheet(SHEET_ID, cell_range, [[result]])

        await ctx.send(f"Updated {player1} vs {player2} result: {result}")

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(ScoreUpdater(bot))
