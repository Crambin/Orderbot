import logging
import discord
from discord.ext import commands
import constants

logger = logging.getLogger(__name__)


class PrettyHelpCommand(commands.MinimalHelpCommand):
    def __init__(self):
        super().__init__(verify_checks=False)

        self.max_command_length = 12
        self.embed_space = "\u200b "

    def get_opening_note(self):
        return None

    def get_ending_note(self):
        ctx = self.context
        if ctx.guild:
            prefix = ctx.bot.guild_prefixes.get(ctx.guild.id, constants.default_prefix)
        else:
            prefix = constants.default_prefix

        command_ = f"{prefix}{self.invoked_with}"
        return (f"Type {command_} <command> for more info on a command.\n"
                f"You can also type {command_} <category> for more info on a category.")

    def add_bot_commands_formatting(self, commands_, heading):
        if commands_:
            joined = "\n".join(f"`{c.name}{self.embed_space * (self.max_command_length - len(c.name))}` - {c.short_doc}"
                               for c in commands_)
            self.paginator.add_line(f"\n**__{heading}__**")
            self.paginator.add_line(joined)

    def add_subcommand_formatting(self, c):
        fmt = f"`{c.name}{self.embed_space * (self.max_command_length - len(c.name))}` - {c.short_doc}"
        self.paginator.add_line(fmt)

    async def send_pages(self):
        destination = self.get_destination()
        if self.context.guild:
            colour = self.context.me.top_role.colour
        else:
            colour = discord.Colour.gold()

        for page in self.paginator.pages:
            embed = discord.Embed(title=discord.Embed.Empty, description=page, colour=colour)
            await destination.send(embed=embed)


class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._original_help_command = bot.help_command
        bot.help_command = PrettyHelpCommand()
        bot.help_command.cog = self

    def cog_unload(self):
        # Revert to default help command in case cog is unloaded.
        self.bot.help_command = self._original_help_command


def setup(bot):
    bot.add_cog(Help(bot))
