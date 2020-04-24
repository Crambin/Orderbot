from discord.ext import commands
import constants


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def prefix(self, ctx, *, prefix=None):
        if prefix is None:
            prefix = self.bot.guild_prefixes[ctx.guild.id]
            await ctx.send(f"The command prefix is `{prefix}`\n"
                           f"To run commands, use `{prefix}command` or do `@{self.bot.user}` command")
            return
        elif prefix == "default":
            prefix = constants.default_prefix

        prefix = prefix.strip()
        if len(prefix) > 15:
            await ctx.send("Prefix must be 15 characters or less.")
            return

        self.bot.guild_prefixes[ctx.guild.id] = prefix
        self.bot.db.update_guild(ctx.guild.id, prefix)
        await ctx.send(f"The command prefix has been changed to `{prefix}`\n"
                       f"To run commands, use `{prefix}command` or do `@{self.bot.user}` command")


def setup(bot):
    bot.add_cog(Moderation(bot))
