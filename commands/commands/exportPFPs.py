import discord
from discord.ext import commands
import os
import aiohttp
import zipfile
import shutil

# Directory to save profile pictures
PFP_DIRECTORY = "exported_pfps"
ZIP_FILE = "pfps_export.zip"

# Ensure the directory exists
if not os.path.exists(PFP_DIRECTORY):
    os.makedirs(PFP_DIRECTORY)

# Define the exportPFPs command
async def setup(bot):
    @bot.command(name="exportPFPs")
    @commands.has_permissions(administrator=True)
    async def export_pfps(ctx):
        """Exports profile pictures of all users in the server and provides a zip file for download."""
        await ctx.send("Exporting profile pictures...")

        # Clear the directory if it already exists
        if os.path.exists(PFP_DIRECTORY):
            shutil.rmtree(PFP_DIRECTORY)
        os.makedirs(PFP_DIRECTORY)

        # Download profile pictures
        async with aiohttp.ClientSession() as session:
            for member in ctx.guild.members:
                avatar_url = member.avatar.url if member.avatar else member.default_avatar.url
                async with session.get(avatar_url) as resp:
                    if resp.status == 200:
                        pfp_data = await resp.read()
                        file_name = f"{PFP_DIRECTORY}/{member.name}_{member.id}.png"
                        with open(file_name, 'wb') as file:
                            file.write(pfp_data)

        # Zip the exported profile pictures
        await ctx.send("Zipping the profile pictures...")
        with zipfile.ZipFile(ZIP_FILE, 'w') as zipf:
            for root, dirs, files in os.walk(PFP_DIRECTORY):
                for file in files:
                    zipf.write(os.path.join(root, file), file)

        # Send the zip file to Discord (if size allows)
        file_size = os.path.getsize(ZIP_FILE)
        max_size = 8 * 1024 * 1024  # 8 MB for regular Discord uploads
        if file_size < max_size:
            await ctx.send("Here is the zip file with the exported profile pictures!", file=discord.File(ZIP_FILE))
        else:
            await ctx.send("The zip file is too large to upload directly to Discord. Please contact the server admin for the file.")

        # Clean up
        shutil.rmtree(PFP_DIRECTORY)
        os.remove(ZIP_FILE)
