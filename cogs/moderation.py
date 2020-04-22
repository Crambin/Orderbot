import json
from discord.ext import commands
import constants


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix=None):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        if prefix is None:
            prefix = prefixes[f"{ctx.guild.id}"]
            await ctx.send(f"The command prefix is `{prefix}`\n"
                           f"To run commands, use `{prefix}command` or do `@{self.bot.user}` command")
            return
        elif prefix == "default":
            prefix = constants.default_prefix

        if len(prefix) > 15:
            await ctx.send("Prefix must be 15 characters or less.")
            return

        prefixes[f"{ctx.guild.id}"] = prefix
        with open('prefixes.json', 'w') as f:
            json.dump(prefixes, f, indent=4)

        await ctx.send(f"The command prefix has been changed to `{prefix}`\n"
                       f"To run commands, use `{prefix}command` or do `@{self.bot.user}` command")


def setup(bot):
    bot.add_cog(Moderation(bot))
