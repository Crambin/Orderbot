import os
import aiohttp
import discord
from discord.ext import commands, tasks


class AdventOfCodeAPI:
    def __init__(self, base_api_url, *, loop, **kwargs):
        self.base_api_url = base_api_url
        self.session = aiohttp.ClientSession(loop=loop, **kwargs)

    async def get_leaderboard(self):
        async with self.session.get(self.base_api_url) as resp:
            return await resp.json()


class AdventOfCode(commands.Cog, command_attrs=dict(hidden=True)):
    def __init__(self, bot):
        self.bot = bot
        self.api = AdventOfCodeAPI("https://adventofcode.com/2020/leaderboard/private/view/877344.json",
                                   loop=self.bot.loop,
                                   cookies={"session": os.getenv("AOC_COOKIE")},
                                   headers={"user-agent": "Orderbot Discord AoC Event Bot"})
        self._leaderboard_cache = None
        self.update_leaderboard_cache.start()

    @tasks.loop(minutes=30)
    async def update_leaderboard_cache(self):
        self._leaderboard_cache = await self.api.get_leaderboard()

    @commands.command()
    async def invite(self, ctx):
        await ctx.send("Join the Durham CS Advent of Code leaderboards here:\n \
                        https://adventofcode.com/2020/leaderboard/private\n \
                        `877344-e32d028c`")

    @commands.command(aliases=["lb"])
    async def leaderboard(self, ctx):
        """
        Shows Advent of Code leaderboard.

        Leaderboard is updated each 30 minutes.
        """
        if self._leaderboard_cache is None:
            return await ctx.send("Please wait - the leaderboard has not been loaded yet.")

        sorted_members = {
            k: v for k, v in sorted(
                self._leaderboard_cache["members"].items(), key=lambda item: item[1]["local_score"], reverse=True
            )
        }

        leaderboard = []
        leaderboard_rank = 0

        for member_data in sorted_members.values():
            leaderboard_rank += 1
            if leaderboard_rank >= 10:
                break

            leaderboard.append(
                f"{leaderboard_rank}) ★ {member_data['stars']:02} | {member_data['local_score']}| {member_data['name']}"
            )

        leaderboard_text = "\n".join(leaderboard)
        embed = discord.Embed(
            description=f"{leaderboard_text}\n\nThe leaderboard is refreshed each 30 minutes.",
            member=ctx.guild.me,
            title="Durham CS AoC leaderboard",
            colour=discord.Colour.gold()
        )
        await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(AdventOfCode(bot))
