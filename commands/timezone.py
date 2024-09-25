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
            await ctx.send(f"Invalid timezone: {timezone}. Please provide a valid timezone.")

    # Command to get the time for a specific player
    @commands.command(name="Time")
    async def get_time(self, ctx, *, player: str = None):
        """Fetches the current time for a player based on their set timezone."""
        if player.startswith("<@"):  # Check if the input is a mention
            # Extract the user ID from the mention
            user_id = int(player[2:-1].replace("!", ""))
            # Find the member using the user ID
            user = ctx.guild.get_member(user_id)
            if user:
                player = user.name
            else:
                await ctx.send("User not found.")
                return

        if player in self.timezones:
            player_timezone = self.timezones[player]
            timezone = pytz.timezone(player_timezone)
            # Format time as Hour:Minutes Day/Month in 24-hour time
            current_time = datetime.now(timezone).strftime('%H:%M %d/%m')

            await ctx.send(f"The current time for {player} in {player_timezone} is {current_time}.")
        else:
            await ctx.send(f"Player '{player}' has not set their timezone. They need to use `!SetTimezone` to set their timezone.")

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(TimeZoneManager(bot))
