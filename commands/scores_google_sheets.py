
import discord
from discord.ext import commands
import gspread
from google.oauth2.service_account import Credentials
import os

# Path to the Google service account JSON file
SERVICE_ACCOUNT_FILE = 'SussyBaka.json'
GOOGLE_SHEET_ID = '1EUS0M_FK4UbUot8xnKpnDS5nOZGT5YV1IXcyg1kf8bI'

# Initialize Google Sheets API credentials and client
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scopes)
client = gspread.authorize(creds)

# Function to access specific worksheet
def get_worksheet(sheet_name):
    sheet = client.open_by_key(GOOGLE_SHEET_ID)
    return sheet.worksheet(sheet_name)

# Read values from a specified range in the worksheet
def read_sheet(sheet_name, range_name):
    worksheet = get_worksheet(sheet_name)
    return worksheet.get(range_name)

# Update values in a specified range in the worksheet
def update_sheet(sheet_name, range_name, values):
    worksheet = get_worksheet(sheet_name)
    cell_list = worksheet.range(range_name)
    for i, cell in enumerate(cell_list):
        cell.value = values[i]
    worksheet.update_cells(cell_list)

class Scores(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.sheet_name = 'Prelim Round Robin'

    @commands.command(name='getscore')
    async def get_score(self, ctx, user: str):
        try:
            data = read_sheet(self.sheet_name, 'A2:B10')
            user_score = next((row[1] for row in data if row[0] == user), None)
            if user_score:
                await ctx.send(f"{user}'s score is {user_score}.")
            else:
                await ctx.send(f"No score found for {user}.")
        except Exception as e:
            await ctx.send("Error retrieving score.")
            print(e)

    @commands.command(name='setscore')
    async def set_score(self, ctx, user: str, score: int):
        try:
            data = read_sheet(self.sheet_name, 'A2:B10')
            cell = next((cell for row in data for cell in row if cell[0] == user), None)
            if cell:
                cell[1] = score
                update_sheet(self.sheet_name, f"A{cell.row}:B{cell.row}", [user, str(score)])
                await ctx.send(f"Updated {user}'s score to {score}.")
            else:
                await ctx.send(f"Could not find {user} to update score.")
        except Exception as e:
            await ctx.send("Error updating score.")
            print(e)

def setup(bot):
    bot.add_cog(Scores(bot))
