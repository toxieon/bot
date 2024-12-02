from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="ping")
    async def ping(self, ctx):
        """Check the bot's latency and display it."""
        await ctx.send(f'ToxiBot Online. Latency: {round(self.bot.latency * 1000)}ms')

async def setup(bot):
    await bot.add_cog(Ping(bot))
