import discord
from discord.ext import commands

class VoiceWho(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command to list all members currently in voice channels
    @commands.command(name="Voicewho")
    async def voice_who(self, ctx):
        """Lists all members currently in voice channels."""

        voice_channel_data = []

        # Loop through all the voice channels and find the members
        for channel in ctx.guild.voice_channels:
            members = channel.members
            if members:  # Only add channels with members
                member_list = ", ".join([member.display_name for member in members])
                voice_channel_data.append(f"**{channel.name}:** {member_list}")

        # If no one is in any voice channels
        if not voice_channel_data:
            await ctx.send("No one is currently in a voice channel.")
            return

        # Format and send the response with the list of users in each voice channel
        voice_channel_info = "\n".join(voice_channel_data)
        await ctx.send(f"Here are the members currently in voice channels:\n{voice_channel_info}")

# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(VoiceWho(bot))
