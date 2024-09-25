import discord
from discord.ext import commands
import os
import aiohttp

# Directory to save profile pictures
PFP_DIRECTORY = "exported_pfps"

# Ensure the directory exists
if not os.path.exists(PFP_DIRECTORY):
    os.makedirs(PFP_DIRECTORY)

# Define the exportPFPs command
async def setup(bot):
    @bot.command(name="exportPFPs")
    @commands.has_permissions(administrator=True)
    async def export_pfps(ctx):
        """Exports profile pictures of all users in the server."""
        await ctx.send("Exporting profile pictures...")

        async with aiohttp.ClientSession() as session:
            for member in ctx.guild.members:
                avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
                async with session.get(avatar_url) as resp:
                    if resp.status == 200:
                        pfp_data = await resp.read()
                        file_name = f"{PFP_DIRECTORY}/{member.name}_{member.id}.png"
                        with open(file_name, 'wb') as file:
                            file.write(pfp_data)

        await ctx.send(f"Profile pictures exported to the `{PFP_DIRECTORY}` folder!")
