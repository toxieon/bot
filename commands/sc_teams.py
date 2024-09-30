import discord
from discord.ext import commands
import random

class SCTeams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scteams")
    async def sc_teams(self, ctx, num_teams: int):
        """Randomly divide people in voice channels into teams."""
        # Check if the user is in a voice channel
        if ctx.author.voice and ctx.author.voice.channel:
            # Get the voice channel the user is in
            voice_channel = ctx.author.voice.channel
            members = voice_channel.members

            if len(members) < num_teams:
                await ctx.send("There are not enough people in the voice channel to make that many teams.")
                return

            # Shuffle and divide members into teams
            random.shuffle(members)
            teams = [[] for _ in range(num_teams)]

            for i, member in enumerate(members):
                teams[i % num_teams].append(member.display_name)

            # Display the teams
            team_msg = ""
            for i, team in enumerate(teams, start=1):
                team_msg += f"**Team {i}:** {', '.join(team)}\n"

            await ctx.send(f"Here are the randomly assigned teams:\n{team_msg}")

        else:
            await ctx.send("You must be in a voice channel to use this command.")


async def setup(bot):
    await bot.add_cog(SCTeams(bot))
