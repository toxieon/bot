import discord
from discord.ext import commands
import json
import os

# File to store user security levels
SECURITY_LEVELS_FILE = "security_levels.json"

# Load security levels from the file
def load_security_levels():
    if os.path.exists(SECURITY_LEVELS_FILE):
        with open(SECURITY_LEVELS_FILE, 'r') as file:
            return json.load(file)
    return {}

# Save security levels to the file
def save_security_levels(security_levels):
    with open(SECURITY_LEVELS_FILE, 'w') as file:
        json.dump(security_levels, file)

# Initialize security levels
user_security_levels = load_security_levels()

class SecurityManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Only the owner can run this command
    @commands.command(name="security")
    @commands.is_owner()
    async def set_security(self, ctx, *args):
        """Set security levels for users. Format: !security <level> user1, user2 or !security <level1> user1, <level2> user2"""
        if len(args) == 0:
            await ctx.send("Please provide a level and one or more users.")
            return

        current_level = None
        i = 0
        while i < len(args):
            # If it's a number, treat it as the current level
            if args[i].isdigit():
                current_level = int(args[i])
            else:
                # If it's a user mention or name, set their security level
                user_name = args[i].replace(",", "")
                user_security_levels[user_name] = current_level or 5  # Default to 5 if no level specified
            i += 1

        # Save the updated security levels
        save_security_levels(user_security_levels)
        await ctx.send(f"Updated security levels: {user_security_levels}")

    # Command to list all users and their security levels
    @commands.command(name="security_list")
    @commands.is_owner()
    async def list_security(self, ctx):
        """List all users and their security levels."""
        if not user_security_levels:
            await ctx.send("No users have been assigned security levels.")
            return

        security_list = "\n".join([f"{user}: Level {level}" for user, level in user_security_levels.items()])
        await ctx.send(f"Users and their security levels:\n{security_list}")

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(SecurityManager(bot))

