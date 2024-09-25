import discord
from discord.ext import commands
import os
import webserver

# Load the bot token from environment variables.
# You'll need to set this variable before running the bot.
# On Windows: `set discordkey=YOUR_BOT_TOKEN`
# On macOS/Linux: `export discordkey=YOUR_BOT_TOKEN`
DISCORD_TOKEN = os.environ.get('discordkey')

# Initialize bot with message content intent
intents = discord.Intents.default()
intents.message_content = True
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

    # Wait for user's response
    role_color_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)

    role_color_input = role_color_msg.content.strip().lower()  # Get the color name and normalize to lowercase

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
    except TimeoutError:
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


# Run the bot
webserver.keep_alive()
bot.run(DISCORD_TOKEN)
