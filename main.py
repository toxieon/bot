import discord
from discord.ext import commands
import os
import webserver

DISCORD_TOKEN = os.environ.get('discordkey')

# Configure bot intents
intents = discord.Intents.default()
intents.members = True
intents.message_content = True  # Important: Enable this for handling commands like !Ping, !Role

bot = commands.Bot(command_prefix='!', intents=intents)

# Initial color options with corresponding emojis
INITIAL_COLOR_OPTIONS = {
    '🟥': ('red', discord.Color.red()),
    '🟦': ('blue', discord.Color.blue()),
    '🟩': ('green', discord.Color.green()),
    '🟨': ('yellow', discord.Color.gold()),
    '🟧': ('orange', discord.Color.orange()),
    '🟪': ('purple', discord.Color.purple()),
    '⬜': ('white', discord.Color.lighter_grey()),
    '⬛': ('black', discord.Color.default()),
    '⬇️': ('more', None),  # Arrow emoji for more options
}

# Additional color options with corresponding emojis
ADDITIONAL_COLOR_OPTIONS = {
    '🟫': ('brown', discord.Color.dark_orange()),
    '🟪': ('violet', discord.Color.purple()),
    '🟡': ('gold', discord.Color.gold()),
    '🔴': ('crimson', discord.Color.dark_red()),
    '🔵': ('navy', discord.Color.dark_blue()),
    '🟤': ('chocolate', discord.Color.dark_gold()),
    '🟣': ('indigo', discord.Color.dark_purple()),
    '🟠': ('amber', discord.Color.orange()),
    '🟦': ('sky blue', discord.Color.blue()),
    '🟩': ('lime', discord.Color.green()),
    '🔶': ('tangerine', discord.Color.orange()),
    '🔷': ('cerulean', discord.Color.blue()),
    '🟥': ('scarlet', discord.Color.red()),
    '⬛': ('onyx', discord.Color.darker_grey())
}


# Ping command to check bot status
@bot.command(name="Ping")
async def ping(ctx):
    await ctx.send("ToxiBot Online")


# Role creation command with emoji-based color selection
@bot.command(name="Role")
async def create_role(ctx):
    """Command to create a role with user-specified name and color via emoji reactions."""

    # Step 1: Ask for role name
    await ctx.send("What would you like the Role name to be?")
    role_name_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
    role_name = role_name_msg.content.strip()  # Get the role name

    # Step 2: Show initial color options and ask for a selection via emoji reactions
    color_prompt = await ctx.send(
        f"Please select a color for **{role_name}** by reacting with one of the emojis below:\n" +
        "🟥 Red\n" +
        "🟦 Blue\n" +
        "🟩 Green\n" +
        "🟨 Yellow\n" +
        "🟧 Orange\n" +
        "🟪 Purple\n" +
        "⬜ White\n" +
        "⬛ Black\n" +
        "⬇️ More Colors")

    # Add emoji reactions for each initial color option
    for emoji in INITIAL_COLOR_OPTIONS.keys():
        await color_prompt.add_reaction(emoji)

    # Function to check the reaction
    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in INITIAL_COLOR_OPTIONS

    try:
        # Wait for the user's reaction
        reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond! Please try again.")
        return

    selected_color_name, selected_color = INITIAL_COLOR_OPTIONS[str(reaction.emoji)]

    # If the user selected the arrow emoji for more colors
    if selected_color_name == 'more':
        # Show additional color options
        additional_color_prompt = await ctx.send(f"More colors for **{role_name}**:\n" +
                                                 "🟫 Brown\n" +
                                                 "🔴 Crimson\n" +
                                                 "🔵 Navy\n" +
                                                 "🟤 Chocolate\n" +
                                                 "🟣 Indigo\n" +
                                                 "🟠 Amber\n" +
                                                 "🟦 Sky Blue\n" +
                                                 "🟩 Lime\n" +
                                                 "🔶 Tangerine\n" +
                                                 "🔷 Cerulean\n" +
                                                 "🟥 Scarlet\n" +
                                                 "⬛ Onyx")

        for emoji in ADDITIONAL_COLOR_OPTIONS.keys():
            await additional_color_prompt.add_reaction(emoji)

        # Wait for the user's reaction for additional colors
        def additional_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ADDITIONAL_COLOR_OPTIONS

        try:
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=additional_check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! Please try again.")
            return

        selected_color_name, selected_color = ADDITIONAL_COLOR_OPTIONS[str(reaction.emoji)]

    # Step 3: Confirmation message
    confirmation = await ctx.send(
        f"Got it! New role **{role_name}** with color **{selected_color_name}**. Does this look correct?")
    await confirmation.add_reaction('✅')
    await confirmation.add_reaction('❌')

    def confirm_check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

    try:
        reaction, _ = await bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)
    except asyncio.TimeoutError:
        await ctx.send("You took too long to respond! Please try again.")
        return

    if str(reaction.emoji) == '✅':
        # Create the role with the selected name and color
        await ctx.guild.create_role(name=role_name, color=selected_color)
        await ctx.send(f'Role "{role_name}" with color {selected_color_name} has been created!')
    else:
        await ctx.send("Role creation canceled.")


# Keep the bot alive using a web server
webserver.keep_alive()

# Run the bot
bot.run(DISCORD_TOKEN)
