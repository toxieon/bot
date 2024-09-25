import discord
from discord.ext import commands

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color_options = {
            '🔴': 'Red',
            '🟢': 'Green',
            '🔵': 'Blue',
            # Add more colors as needed
            '⬆️': 'More Options',  # For more options arrow
        }

    @commands.command(name="Role")
    async def create_role(self, ctx):
        """Creates a role with a specified color."""

        def check_author(message):
            return message.author == ctx.author and message.channel == ctx.channel

        await ctx.send("What would you like the Role name to be? Type 'cancel' at any time to cancel.")
        role_name_msg = await self.bot.wait_for('message', check=check_author)

        if role_name_msg.content.lower() == 'cancel':
            await ctx.send("Role creation canceled.")
            return

        role_name = role_name_msg.content

        # Send the color prompt message
        color_prompt = await ctx.send(f"Please select a color for {role_name} by reacting with one of the emojis below:")

        # Add the reactions for the available colors
        try:
            for emoji in self.color_options:
                await color_prompt.add_reaction(emoji)
        except discord.HTTPException as e:
            await ctx.send(f"Error adding reactions: {e}")
            return

        # Wait for the user to select a reaction
        def reaction_check(reaction, user):
            return user == ctx.author and reaction.message.id == color_prompt.id and str(reaction.emoji) in self.color_options

        reaction, user = await self.bot.wait_for('reaction_add', check=reaction_check)

        if str(reaction.emoji) == '⬆️':
            await ctx.send("You selected more options! (This would load more color choices here.)")
            # Add more options if needed
            return

        selected_color = self.color_options[str(reaction.emoji)]
        await ctx.send(f"Got it, new role {role_name} will be {selected_color}. Does this look correct? (yes/no)")

        # Confirmation for creating the role
        confirmation_msg = await self.bot.wait_for('message', check=check_author)

        if confirmation_msg.content.lower() == 'yes':
            await ctx.guild.create_role(name=role_name, colour=discord.Colour.from_str(selected_color.lower()))
            await ctx.send(f"Role {role_name} with color {selected_color} created!")
        else:
            await ctx.send("Role creation canceled.")
