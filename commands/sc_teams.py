import discord
from discord.ext import commands
import random

class SCTeams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scteams")
    async def sc_teams(self, ctx, num_teams: int):
        """Command to randomly divide users in a voice call into teams."""
        voice_channel = ctx.author.voice.channel

        if voice_channel is None:
            await ctx.send("You are not in a voice channel.")
            return

        members = voice_channel.members
        random.shuffle(members)

        teams = [[] for _ in range(num_teams)]
        for i, member in enumerate(members):
            teams[i % num_teams].append(member.display_name)

        response = ""
        for i, team in enumerate(teams, 1):
            response += f"**Team {i}:**\n" + "\n".join(team) + "\n\n"

        await ctx.send(response)

# Setup function to add this Cog
async def setup(bot):
    await bot.add_cog(SCTeams(bot))
