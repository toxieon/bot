import discord
from discord.ext import commands

# Define the Ping command
async def setup(bot):
    @bot.command(name="Ping")
    async def ping(ctx):
        """Simple ping command to check if the bot is online."""
        await ctx.send("ToxiBot Online")
