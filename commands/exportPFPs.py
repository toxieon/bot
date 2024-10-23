import discord
from discord.ext import commands
import os
import aiohttp
import zipfile
import shutil

# Directory to save profile pictures
PFP_DIRECTORY = "exported_pfps"
ZIP_FILE_PREFIX = "pfps_export"
MAX_DISCORD_FILE_SIZE = 8 * 1024 * 1024  # 8MB for standard Discord users

# Define the exportPFPs command
async def setup(bot):
    @bot.command(name="exportPFPs")
    @commands.has_permissions(administrator=True)
    async def export_pfps(ctx):
        """Exports profile pictures of all users in the server and provides them in multiple zip files if needed."""
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

        # Zip the profile pictures in batches
        await ctx.send("Zipping the profile pictures into multiple files if necessary...")

        zip_file_count = 1
        total_file_size = 0
        current_zip_files = []
        zip_file_path = f"{ZIP_FILE_PREFIX}_{zip_file_count}.zip"

        with zipfile.ZipFile(zip_file_path, 'w') as zipf:
            for root, dirs, files in os.walk(PFP_DIRECTORY):
                for file in files:
                    file_path = os.path.join(root, file)
                    file_size = os.path.getsize(file_path)

                    # If adding this file would exceed the Discord limit, start a new zip file
                    if total_file_size + file_size > MAX_DISCORD_FILE_SIZE:
                        # Close the current zip file and start a new one
                        zipf.close()
                        current_zip_files.append(zip_file_path)

                        # Send the current zip file
                        await ctx.send(f"Here is the zip file #{zip_file_count} with exported profile pictures!", file=discord.File(zip_file_path))

                        # Reset for the new zip file
                        zip_file_count += 1
                        zip_file_path = f"{ZIP_FILE_PREFIX}_{zip_file_count}.zip"
                        zipf = zipfile.ZipFile(zip_file_path, 'w')
                        total_file_size = 0

                    # Add the current file to the zip
                    zipf.write(file_path, file)
                    total_file_size += file_size

            # Close and save the last zip file
            zipf.close()
            current_zip_files.append(zip_file_path)

            # Send the last zip file
            await ctx.send(f"Here is the zip file #{zip_file_count} with exported profile pictures!", file=discord.File(zip_file_path))

        # Clean up after sending the zip files
        shutil.rmtree(PFP_DIRECTORY)
        for zip_file in current_zip_files:
            os.remove(zip_file)
