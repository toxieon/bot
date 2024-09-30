import discord
from discord.ext import commands
import random

class SCTeams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scteams")
    async def sc_teams(self, ctx, num_teams: int):
        """Command to randomly divide users in a voice call into teams."""
        try:
            # Check if the user is in a voice channel
            if ctx.author.voice is None or ctx.author.voice.channel is None:
                await ctx.send("You are not in a voice channel.")
                return

            voice_channel = ctx.author.voice.channel
            members = voice_channel.members

            # Check if there are any members in the voice channel
            if len(members) == 0:
                await ctx.send("There are no members in your voice channel.")
                return

            random.shuffle(members)

            # Check if the number of teams is valid
            if num_teams <= 0 or num_teams > len(members):
                await ctx.send(f"Invalid number of teams. You must choose a number between 1 and {len(members)}.")
                return

            # Create teams
            teams = [[] for _ in range(num_teams)]
            for i, member in enumerate(members):
                teams[i % num_teams].append(member.display_name)

            # Prepare the response message
            response = ""
            for i, team in enumerate(teams, 1):
                response += f"**Team {i}:**\n" + "\n".join(team) + "\n\n"

            await ctx.send(response)

        except Exception as e:
            await ctx.send(f"An error occurred: {e}")

# Setup function to add this Cog
async def setup(bot):
    await bot.add_cog(SCTeams(bot))
