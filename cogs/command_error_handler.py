import traceback
import logging
import discord
from discord.ext import commands

logger = logging.getLogger(__name__)


class CommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error_):
        # If command has local error handler, return
        if hasattr(ctx.command, "on_error"):
            return

        # Get the original exception
        error = getattr(error_, "original", error_)

        if isinstance(error, commands.CommandNotFound):
            return

        elif isinstance(error, commands.UserInputError):
            await ctx.send(f"Invalid command input: {error}")

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send("This command cannot be used in direct messages.")
            except discord.Forbidden:
                return

        # this will only return if it is a DM forbidden error
        elif isinstance(error, discord.errors.Forbidden) and error.code == 50007:
            return

        elif isinstance(error, (commands.MissingPermissions, commands.BotMissingPermissions)):
            missing = [perm.replace("_", " ").replace("guild", "server").title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = f"{'**, **'.join(missing[:-1])}, and {missing[-1]}"
            else:
                fmt = " and ".join(missing)
            message = "You " if isinstance(error, commands.MissingPermissions) else "I "
            message += f"need the **{fmt}** permission(s) to use this command."
            await ctx.send(message)

        elif isinstance(error, commands.CheckFailure):
            if error.args:
                await ctx.send(". ".join(error.args))
            else:
                await ctx.send("You do not have permission to use this command.")

        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command has been disabled.")

        else:
            exception_msg = f"Ignoring exception in command {ctx.command} error: {traceback.format_exc()}"
            logger.warning(exception_msg)
            await self.bot.log_error(exception_msg)


def setup(bot):
    bot.add_cog(CommandErrorHandler(bot))
