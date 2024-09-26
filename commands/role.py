import discord
from discord.ext import commands

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color_emojis = {
            '🟥': discord.Color.red(),
            '🟦': discord.Color.blue(),
            '🟩': discord.Color.green(),
            # Add more color emoji mappings here
        }
        self.expanded_color_emojis = {
            '🟧': discord.Color.orange(),
            '🟨': discord.Color.gold(),
            '🟪': discord.Color.purple(),
            '⬆️': 'expand_more',  # Arrow to show more options
            # Add more emojis for more colors here
        }

    @commands.command(name="Role")
    async def create_role(self, ctx):
        """Create a new role with user-specified name and color."""
        await ctx.send("What would you like the Role name to be? Type 'cancel' at any time to cancel.")

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        try:
            # Wait for the role name response
            role_name_msg = await self.bot.wait_for('message', check=check)
            role_name = role_name_msg.content

            # If user types 'cancel'
            if role_name.lower() == 'cancel':
                await ctx.send("Role creation canceled.")
                return

            await ctx.send(f"Please select a color for {role_name} by reacting with one of the emojis below:")

            # Send color prompt message
            color_prompt = await ctx.send("React with your desired color below:")

            # Initial reactions for colors
            for emoji in self.color_emojis:
                await color_prompt.add_reaction(emoji)

            def reaction_check(reaction, user):
                return user == ctx.author and str(reaction.emoji) in self.color_emojis

            reaction, _ = await self.bot.wait_for('reaction_add', check=reaction_check)
            selected_color = self.color_emojis[str(reaction.emoji)]

            # Check if the user selected the "expand_more" emoji for more colors
            if str(reaction.emoji) == '⬆️':
                await ctx.send("Expanding to show more colors...")
                for emoji in self.expanded_color_emojis:
                    await color_prompt.add_reaction(emoji)

                # Check again for additional reaction
                reaction, _ = await self.bot.wait_for('reaction_add', check=reaction_check)
                selected_color = self.expanded_color_emojis.get(str(reaction.emoji), selected_color)

            # Ask user to confirm
            await ctx.send(f"Got it! New role {role_name} will be {str(selected_color)}. Does this look correct? (yes/no)")

            confirm_msg = await self.bot.wait_for('message', check=check)
            if confirm_msg.content.lower() == 'yes':
                await ctx.guild.create_role(name=role_name, color=selected_color)
                await ctx.send(f"Role '{role_name}' has been created!")
            else:
                await ctx.send("Role creation canceled.")

        except Exception as e:
            await ctx.send(f"An error occurred: {str(e)}")

# Add the setup function to register the cog
async def setup(bot):
    await bot.add_cog(RoleManager(bot))
