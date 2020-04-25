import discord
from discord.ext import commands
from utils import embed, checks


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.bot_has_permissions(manage_messages=True)
    @commands.guild_only()
    async def purge(self, ctx, num_messages: int):
        """
        Removes messages in bulk.
        This is limited to a maximum of 100 messages.
        """
        if not 1 <= num_messages <= 100:
            await ctx.send("Number of messages to delete must be between 1 and 100.")
            return

        # TODO: Custom checks
        num_deleted = len(await ctx.channel.purge(limit=num_messages+1))-1
        formatted_num_deleted = f"{num_deleted} message" + ("." if num_deleted == 1 else 's.')
        await ctx.send(f"{ctx.author.mention} Deleted {formatted_num_deleted}", delete_after=5)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    @commands.guild_only()
    async def warn(self, ctx, member: discord.Member, *, reason="No reason specified."):
        """
        Warns a selected member in this server.
        A reason can be attached if specified.
        """
        if ctx.author == member or member == ctx.guild.me:
            return

        dm_embed = embed.infraction(member, 'Warn', reason, dm=True)
        dm_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if not member.bot:
            try:
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass

        await ctx.send(embed=embed.infraction(member, 'Warn', reason))

    @commands.command()
    @commands.has_permissions(kick_members=True)
    @commands.bot_has_permissions(kick_members=True)
    @commands.guild_only()
    async def kick(self, ctx, member: discord.Member, *, reason="No reason specified."):
        """
        Kicks a selected member from this server.
        A reason can be attached if specified.
        """
        if ctx.author == member or member == ctx.guild.me:
            return

        checks.is_invoker_role_higher(ctx, member)
        if not checks.is_bot_role_higher(ctx, member):
            await ctx.send("I am not allowed to kick this user unless my role is above theirs.")
            return

        dm_embed = embed.infraction(member, 'Kick', reason, dm=True)
        dm_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if not member.bot:
            try:
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass

        await member.kick(reason=reason)
        await ctx.send(embed=embed.infraction(member, 'Kick', reason))

    @commands.command()
    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.guild_only()
    async def ban(self, ctx, member: discord.Member, *, reason="No reason specified."):
        """
        Permanently bans a selected member from this server.
        A reason can be attached if specified.
        """
        if ctx.author == member or member == ctx.guild.me:
            return

        checks.is_invoker_role_higher(ctx, member)
        if not checks.is_bot_role_higher(ctx, member):
            await ctx.send("I am not allowed to ban this user unless my role is above theirs.")
            return

        # TODO: Custom, user-defined durations
        duration = 'Permanent'
        dm_embed = embed.infraction(member, 'Ban', reason, duration=duration, dm=True)
        dm_embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        if not member.bot:
            try:
                await member.send(embed=dm_embed)
            except discord.Forbidden:
                pass

        await member.ban(reason=reason)
        await ctx.send(embed=embed.infraction(member, 'Ban', reason, duration=duration))


def setup(bot):
    bot.add_cog(Moderation(bot))
