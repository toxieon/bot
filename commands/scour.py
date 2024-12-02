from datetime import datetime, timedelta

from discord.ext import commands

async def scour(ctx, extension: str, days: int):
    """Scour the channel for files with a specific extension uploaded in the past 'days' days."""
    if not extension.startswith('.'):
        await ctx.send("Please provide a valid file extension starting with a dot (e.g., .txt, .png).")
        return

    # Calculate the time threshold
    time_threshold = datetime.utcnow() - timedelta(days=days)

    matching_files = []

    # Fetch messages from the channel's history
    async for message in ctx.channel.history(after=time_threshold):
        for attachment in message.attachments:
            if attachment.filename.endswith(extension):
                matching_files.append(attachment.url)

    if matching_files:
        response = "Found the following files:\n" + "\n".join(matching_files)
    else:
        response = f"No files with the extension '{extension}' found in the past {days} days."

    await ctx.send(response)

# Define the setup function to add the command
def setup(bot):
    @bot.command(name="Scour")
    async def scour_command(ctx, extension: str, days: int):
        await scour(ctx, extension, days)
