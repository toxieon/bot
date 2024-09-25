import discord
from discord.ext import commands
import pytz
from datetime import datetime
import json
import os

# File to store user timezones
TIMEZONE_FILE = "timezones.json"

class TimeZoneManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.timezones = self.load_timezones()

    # Load the timezone data from a file
    def load_timezones(self):
        if os.path.exists(TIMEZONE_FILE):
            with open(TIMEZONE_FILE, 'r') as file:
                return json.load(file)
        return {}

    # Save the timezone data to a file
    def save_timezones(self):
        with open(TIMEZONE_FILE, 'w') as file:
            json.dump(self.timezones, file)

    # Command to set a user's timezone
    @commands.command(name="SetTimezone")
    async def set_timezone(self, ctx, timezone: str):
        """Allows users to set their timezone."""
        try:
            # Validate the timezone input
            pytz.timezone(timezone)
            self.timezones[ctx.author.name] = timezone
            self.save_timezones()
            await ctx.send(f"Timezone for {ctx.author.name} set to {timezone}.")
        except pytz.UnknownTimeZoneError:
            await ctx.send(f"Invalid timezone: {timezone}. Please provide a valid timezone from the IANA timezone database.")

    # Command to get the time for a specific player
    @commands.command(name="Time")
    async def get_time(self, ctx, player: str):
        """Fetches the current time for a player based on their set timezone."""
        if player in self.timezones:
            player_timezone = self.timezones[player]
            timezone = pytz.timezone(player_timezone)
            current_time = datetime.now(timezone).strftime('%Y-%m-%d %H:%M:%S')

            await ctx.send(f"The current time for {player} in {player_timezone} is {current_time}.")
        else:
            await ctx.send(f"Player '{player}' has not set their timezone. They need to use `!SetTimezone` to set their timezone.")

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(TimeZoneManager(bot))
