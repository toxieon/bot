import discord
from discord.ext import commands

COLOR_OPTIONS = {
    '🟥': ('red', discord.Color.red()),
    '🟦': ('blue', discord.Color.blue()),
    '🟩': ('green', discord.Color.green()),
    '🟨': ('yellow', discord.Color.gold()),
    '🟧': ('orange', discord.Color.orange()),
    '🟪': ('purple', discord.Color.purple()),
    '⬜': ('white', discord.Color.lighter_grey()),
    '⬛': ('black', discord.Color.default())
}


# Define the Role command
async def setup(bot):
    @bot.command(name="Role")
    async def create_role(ctx):
        """Command to create a role with user-specified name and color via emoji reactions."""

        # Step 1: Ask for role name
        await ctx.send("What would you like the Role name to be?")
        role_name_msg = await bot.wait_for('message', check=lambda message: message.author == ctx.author)
        role_name = role_name_msg.content.strip()  # Get the role name

        # Step 2: Show color options and ask for a selection via emoji reactions
        color_prompt = await ctx.send(
            f"Please select a color for **{role_name}** by reacting with one of the emojis below:\n" +
            "🟥 Red\n" +
            "🟦 Blue\n" +
            "🟩 Green\n" +
            "🟨 Yellow\n" +
            "🟧 Orange\n" +
            "🟪 Purple\n" +
            "⬜ White\n" +
            "⬛ Black")

        # Add emoji reactions for each color
        for emoji in COLOR_OPTIONS.keys():
            await color_prompt.add_reaction(emoji)

        # Function to check the reaction
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in COLOR_OPTIONS

        try:
            # Wait for the user's reaction
            reaction, _ = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! Please try again.")
            return

        selected_color_name, selected_color = COLOR_OPTIONS[str(reaction.emoji)]

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
