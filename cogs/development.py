import os
import psutil
import datetime
from discord.ext import commands

from utils import checks
import utils


class Development(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process(os.getpid())

    @commands.command(aliases=('delbday',))
    @commands.check(checks.is_bot_developer)
    async def del_bday(self, ctx, *, query=None):
        user = await utils.get_user_from_message(ctx, query)
        await self.bot.db.user.delete_birthday(user.id)
        await ctx.send(f"User {user} has been deleted from the birthdays db.")

    @commands.command()
    @commands.check(checks.is_bot_developer)
    async def uptime(self, ctx):
        """
        Show current uptime of the bot.
        This is currently a developer-only command.
        """
        uptime = datetime.datetime.now() - self.bot.start_time
        days = uptime.days
        hours, remainder = divmod(uptime.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        formatted_uptime = "The bot has been running for "
        for value, name in zip((days, hours, minutes, seconds), ('day', 'hour', 'minute', 'second')):
            if value:
                formatted_uptime += f"{value} {name}" + (", " if value == 1 else "s, ")
        formatted_uptime = formatted_uptime.rsplit(',', 1)[0] + '.'
        formatted_uptime = ' and'.join(formatted_uptime.rsplit(',', 1))

        await ctx.send(formatted_uptime)

    @commands.command()
    @commands.cooldown(1, 10, commands.BucketType.guild)
    @commands.check(checks.is_bot_developer)
    async def process_stats(self, ctx):
        """
        Show bot information about processes and memory usage.
        This is currently a developer-only command.
        """
        bot_ram_usage = self.process.memory_full_info().rss / 1024 ** 2
        bot_ram_usage = f"{bot_ram_usage:.2f} MB"

        virtual_memory = psutil.virtual_memory()
        server_ram_usage = f"{virtual_memory.used / 1024 / 1024:.0f} MB"
        total_server_ram = f"{virtual_memory.total / 1024 / 1024:.0f} MB"

        cpu_count = psutil.cpu_count()

        bot_cpu_usage = self.process.cpu_percent()
        if bot_cpu_usage > 100:
            bot_cpu_usage = bot_cpu_usage / cpu_count

        server_cpu_usage = psutil.cpu_percent()
        if server_cpu_usage > 100:
            server_cpu_usage = server_cpu_usage / cpu_count

        io_counters = self.process.io_counters()
        io_read_bytes = f"{io_counters.read_bytes / 1024 / 1024:.3f}MB"
        io_write_bytes = f"{io_counters.write_bytes / 1024 / 1024:.3f}MB"

        msg = (f"Bot RAM usage: {bot_ram_usage}\n"
               f"Server RAM usage: {server_ram_usage}\n"
               f"Total server RAM: {total_server_ram}\n"
               f"Bot CPU usage: {bot_cpu_usage}\n"
               f"Server CPU usage: {server_cpu_usage}\n"
               f"IO (r/w): {io_read_bytes} / {io_write_bytes}")

        await ctx.send(f"```{msg}```")


def setup(bot):
    bot.add_cog(Development(bot))
