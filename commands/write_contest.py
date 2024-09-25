from discord.ext import commands
import datetime


class WriteContest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="WriteContest")
    async def write_contest(self, ctx, *, contest_name=None):
        """Generates a contest announcement with the given contest name."""

        # Check if the contest name was provided
        if contest_name is None:
            await ctx.send(
                "Please provide a contest name. Usage: `!WriteContest <contest_name>`\nExample: `!WriteContest Halloween Special`")
            return

        # Get the current date
        current_date = datetime.date.today().strftime('%B %d, %Y')

        # Template for the contest announcement
        announcement = (
            f"🎉 **Next Event: {contest_name}!** 🎉\n\n"
            f"📅 Date: {current_date}\n"
            "Here are the features of the upcoming event:\n"
            "• Exciting challenges\n"
            "• Amazing prizes\n"
            "• Fun for everyone\n"
            "\nMake sure to mark your calendars and participate!"
        )

        # Send the generated announcement
        await ctx.send(announcement)


# Setup function to add the cog
async def setup(bot):
    await bot.add_cog(WriteContest(bot))
