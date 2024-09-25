import discord
from discord.ext import commands
import os
import webserver

# Load the bot token from environment variables
DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()  # Default intents
intents.members = True  # Enable members intent if you need access to guild member updates
intents.presences = False  # Disable presence intent if you don't need to track users' online statuses

bot = commands.Bot(command_prefix='!', intents=intents)

# Dictionary of common color names to RGB tuples
COLOR_DICT = {
    'red': discord.Color.red(),
    'blue': discord.Color.blue(),
    'green': discord.Color.green(),
    'yellow': discord.Color.gold(),
    'orange': discord.Color.orange(),
    'purple': discord.Color.purple(),
    'pink': discord.Color.magenta(),
    'black': discord.Color.default(),
    'white': discord.Color.lighter_grey()
}


# Ping command to check bot status
@bot.command(name="Ping")
async def ping(ctx):
    """Simple ping command to check if the bot is online."""
    await ctx.send("ToxiBot Online")


# Role creation command
@bot.command(name="Role")
async def create_role(ctx):
    """Command to create a role with user-specified name and color."""

    # Step 1: Ask for role name
    await ctx.send("What would you like the Role name to be?")

    # Wait for user's response
    role_name_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    role_name = role_name_msg.content.strip()  # Get the role name

    # Step 2: Ask for role color
    await ctx.send(f"What color would you like {role_name} to be? (e.g., red, blue, green, etc.)")
    role_color_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    role_color_input = role_color_msg.content.strip().lower()  # Get the color name

    # Step 3: Find the closest color match from the dictionary
    role_color = COLOR_DICT.get(role_color_input, discord.Color.default())

    # Preview message asking for confirmation
    role_preview = await ctx.send(
        f"Got it! New role **{role_name}** (in {role_color_input} color) – does this look correct?")

    # Add reactions for Yes/No choice
    await role_preview.add_reaction('✅')  # Yes
    await role_preview.add_reaction('❌')  # No

    def check_reaction(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=30.0, check=check_reaction)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond! Please try again.")
        return

    # Step 4: Handle user's confirmation
    if str(reaction.emoji) == '✅':
        # User confirmed, so create the role
        await ctx.guild.create_role(name=role_name, color=role_color)
        await ctx.send(f'Role "{role_name}" with color {role_color_input} has been created!')
    else:
        # User canceled
        await ctx.send("Role creation canceled.")


# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
