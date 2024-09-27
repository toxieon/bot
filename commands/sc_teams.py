import discord
from discord.ext import commands
import random


class StarCraftTeams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to create StarCraft teams based on members in voice channels
    @commands.command(name="ScTeams")
    async def sc_teams(self, ctx):
        """Randomly create StarCraft teams from members in voice channels."""

        # Get the voice channel the bot was pinged in, and check for connected members
        voice_channel_members = []
        for channel in ctx.guild.voice_channels:
            voice_channel_members.extend(channel.members)

        if not voice_channel_members:
            await ctx.send("There are no members currently in any voice channel.")
            return

        # Ask how many teams to create
        await ctx.send("How many teams do you want to create? Please provide a number.")

        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.isdigit()

        try:
            # Wait for the response from the user
            team_msg = await self.bot.wait_for("message", check=check, timeout=30.0)
            num_teams = int(team_msg.content)
        except Exception:
            await ctx.send("You didn't provide a valid number in time. Command cancelled.")
            return

        # Ensure valid team numbers
        if num_teams < 2:
            await ctx.send("You need at least 2 teams.")
            return
        if num_teams > len(voice_channel_members):
            await ctx.send(f"There are not enough members to form {num_teams} teams. Command cancelled.")
            return

        # Shuffle the members randomly
        random.shuffle(voice_channel_members)

        # Split members into teams
        teams = [[] for _ in range(num_teams)]
        for i, member in enumerate(voice_channel_members):
            teams[i % num_teams].append(member)

        # Format and display the teams
        result = "Here are the randomly generated teams:\n"
        for i, team in enumerate(teams, 1):
            result += f"**Team {i}:** " + ", ".join([member.display_name for member in team]) + "\n"

        await ctx.send(result)


# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(StarCraftTeams(bot))
