import discord
from discord.ext import commands

# Define the available color options and the arrow for more options
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

ADDITIONAL_COLOR_OPTIONS = {
    '🟫': ('brown', discord.Color.dark_orange()),
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


class RoleCreator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="Role")
    async def create_role(self, ctx):
        """Command to create a role with user-specified name and color via emoji reactions."""

        # Step 1: Ask for role name
        await ctx.send("What would you like the Role name to be? Type 'cancel' at any time to cancel.")
        role_name_msg = await self.bot.wait_for('message', check=lambda message: message.author == ctx.author)

        # Check if the user typed "cancel"
        if role_name_msg.content.lower() == 'cancel':
            await ctx.send("Role creation process canceled.")
            return

        role_name = role_name_msg.content.strip()

        # Step 2: Show clean color prompt
        color_prompt = await ctx.send(
            f"Please select a color for **{role_name}** by reacting with one of the emojis below:")

        # Add all reactions at once
        emojis = list(INITIAL_COLOR_OPTIONS.keys())
        await color_prompt.add_reactions(emojis)

        def reaction_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in INITIAL_COLOR_OPTIONS

        # Wait for a reaction
        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=reaction_check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! Process canceled.")
            return

        selected_color_name, selected_color = INITIAL_COLOR_OPTIONS[str(reaction.emoji)]

        # Handle the "more" arrow for additional color options
        if selected_color_name == 'more':
            # Show additional color options
            additional_color_prompt = await ctx.send(f"Here are more colors for **{role_name}**:")
            more_emojis = list(ADDITIONAL_COLOR_OPTIONS.keys())
            await additional_color_prompt.add_reactions(more_emojis)

            def additional_check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in ADDITIONAL_COLOR_OPTIONS

            try:
                reaction, _ = await self.bot.wait_for('reaction_add', timeout=60.0, check=additional_check)
            except asyncio.TimeoutError:
                await ctx.send("You took too long to respond! Process canceled.")
                return

            selected_color_name, selected_color = ADDITIONAL_COLOR_OPTIONS[str(reaction.emoji)]

        # Step 3: Confirmation message
        confirmation_msg = await ctx.send(
            f"Got it! New role **{role_name}** with color **{selected_color_name}**.\nDoes this look correct? React with ✅ to confirm or ❌ to cancel.")
        await confirmation_msg.add_reaction('✅')
        await confirmation_msg.add_reaction('❌')

        def confirm_check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in ['✅', '❌']

        try:
            reaction, _ = await self.bot.wait_for('reaction_add', timeout=30.0, check=confirm_check)
        except asyncio.TimeoutError:
            await ctx.send("You took too long to respond! Process canceled.")
            return

        if str(reaction.emoji) == '✅':
            # Create the role with the selected name and color
            await ctx.guild.create_role(name=role_name, color=selected_color)
            await ctx.send(f'Role "{role_name}" with color {selected_color_name} has been created!')
        else:
            await ctx.send("Role creation process canceled.")


# Setup function to properly add the cog
async def setup(bot):
    await bot.add_cog(RoleCreator(bot))
