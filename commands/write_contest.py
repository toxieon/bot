from discord.ext import commands
import datetime


# Define the WriteContest command
async def setup(bot):
    @bot.command(name="WriteContest")
    async def write_contest(ctx, *, contest_name):
        """Generates a contest announcement with the given contest name."""

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
