from discord.ext import commands


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def ping(self, ctx):
        message = await ctx.send("Pong!")
        time_taken = (message.created_at - ctx.message.created_at).microseconds / 1000
        await message.edit(content=f"Pong! Latency is {time_taken:.0f}ms. "
                                   f"API latency is {self.bot.latency*1000:.0f}ms")


def setup(bot):
    bot.add_cog(Other(bot))
