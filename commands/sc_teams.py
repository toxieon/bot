import discord
from discord.ext import commands
import random

class StarCraftTeams(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="scteams")
    async def scteams(self, ctx, num_teams: int):
        """Randomly assigns people in voice channels into teams."""
        voice_channels = ctx.guild.voice_channels
        participants = []

        # Gather all users from all voice channels
        for channel in voice_channels:
            participants += channel.members

        if len(participants) < num_teams:
            await ctx.send("Not enough people in voice channels to make that many teams.")
            return

        # Shuffle participants and divide into teams
        random.shuffle(participants)
        teams = [[] for _ in range(num_teams)]
        for i, participant in enumerate(participants):
            teams[i % num_teams].append(participant.display_name)

        # Create team message
        team_message = "Here are the teams:\n"
        for idx, team in enumerate(teams):
            team_message += f"**Team {idx + 1}:** {', '.join(team)}\n"

        await ctx.send(team_message)

async def setup(bot):
    await bot.add_cog(StarCraftTeams(bot))
