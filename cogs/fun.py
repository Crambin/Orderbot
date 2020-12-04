import os

import async_cleverbot as ac
from discord.ext import commands


class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        api_key = os.getenv('CHATBOT_API_KEY')
        self.chat_bot = ac.Cleverbot(api_key, context=ac.DictContext()) if api_key else None
        self.is_talking = {}

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        elif message.channel.id not in self.is_talking.get(message.author.id, set()):
            return
        if 3 <= len(message.content) <= 60:
            resp = await self.chat_bot.ask(message.content, message.channel.id)
            await message.channel.send(resp.text)

    @commands.command()
    async def speak(self, ctx, *, query=None):
        """
        Speak to the chat bot, like Cleverbot.
        """
        if not self.chat_bot:
            return await ctx.send("This command is currently disabled.")
        elif query is None:
            return await ctx.send("You can't talk without saying anything!")

        resp = await self.chat_bot.ask(query, ctx.channel.id)
        await ctx.send(resp.text)

    @commands.command(aliases=('talk', 'toggle'))
    async def toggle_talk(self, ctx):
        """
        Toggle whether the bot will respond to your messages.

        This command is per-user, per-channel, meaning if you use it
        in one channel it will only affect you in that channel, and nobody else.
        """
        self.is_talking[ctx.author.id] = self.is_talking.get(ctx.author.id, set())
        if ctx.channel.id in self.is_talking[ctx.author.id]:
            self.is_talking[ctx.author.id].remove(ctx.channel.id)
            await ctx.send("I will no longer respond to you in this channel.")
        else:
            self.is_talking[ctx.author.id].add(ctx.channel.id)
            await ctx.send("I will now respond to you in this channel.")


def setup(bot):
    bot.add_cog(Fun(bot))
