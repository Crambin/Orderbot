import random
import asyncio
import urllib.request
from discord.ext import commands


class MarkovModel:
    def __init__(self, corpus=None, word_pairs=None):
        self.chain = None
        if word_pairs:
            self.word_dict = word_pairs
        else:
            self.word_dict = {}
            pairs = self.make_pairs(corpus)
            self.create_word_dict(pairs)

    @staticmethod
    def make_pairs(corpus):
        for i in range(len(corpus) - 1):
            yield corpus[i], corpus[i + 1]

    def create_word_dict(self, pairs):
        for first, second in pairs:
            if first in self.word_dict:
                self.word_dict[first].append(second)
            else:
                self.word_dict[first] = [second]

    def append_next_word(self):
        prev_word = self.chain[-1]
        next_word = random.choice(self.word_dict[prev_word])
        self.chain.append(next_word)

    def generate(self, n=None):
        if n is None:
            n = random.randint(5, 40)
        elif not isinstance(n, int):
            raise ValueError("Input must be an integer")
        elif n <= 0:
            return

        first_word = random.choice(list(self.word_dict.keys()))

        self.chain = [first_word]
        for _ in range(n):
            self.append_next_word()

        return ' '.join(self.chain)


class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.markov_models = {}

    @commands.command()
    async def say(self, ctx, *, message):
        """
        Will say whatever the user says.
        """
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    async def ping(self, ctx):
        """
        Pings the discord API for current response time.
        """
        message = await ctx.send("Ping!")
        time_taken = (message.created_at - ctx.message.created_at).microseconds / 1000
        await message.edit(content=f"Pong! Latency is {time_taken:.0f}ms. "
                                   f"API latency is {self.bot.latency * 1000:.0f}ms")

    @commands.command()
    async def tags(self, ctx):
        tags = '`, `'.join(await self.bot.db.markov.get_tags())
        await ctx.send(f"Current tags: \n`{tags}`")

    @commands.command()
    async def markov(self, ctx, *, tag):
        tag = tag.lower()
        if tag in self.markov_models:
            model = self.markov_models.get(tag, None)
        else:
            pairs = await self.bot.db.markov.fetch(tag)
            model = MarkovModel(word_pairs=pairs) if pairs else None

        if model is None:
            await ctx.send("This tag does not exist within the markov database.")
            await self.tags(ctx)
            return

        self.markov_models[tag] = model
        await ctx.send(model.generate())

    # TODO: check against existing tags
    @commands.command()
    async def upload_markov(self, ctx):
        """
        Uses an uploaded {tag}.txt file to make a new markov model.
        Tag must be at most 15 characters.
        :param ctx:
        """
        def check(m):
            return m.author == ctx.message.author and m.channel == ctx.channel

        if len(ctx.message.attachments) == 0:
            await ctx.send("Please send a `{tag}.txt` file now")
            try:
                ctx.message = await self.bot.wait_for('message', check=check, timeout=60)
            except asyncio.TimeoutError:
                await ctx.send("Command has timed out. Please try again.")
                return

        attachments = list(filter(lambda a: a.filename[-3:] == 'txt', ctx.message.attachments))
        if len(attachments) == 0:
            await ctx.send("**Command failed**;\n"
                           "This command requires a dataset to be sent as a .txt attachment.")
            return

        for attachment in attachments:
            tag = attachment.filename[:-4]
            if len(tag) > 20:
                await ctx.send(f"Tag `{tag}` could not be added as it is greater than 15 characters.")
                continue

            req = urllib.request.Request(attachment.url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as f:
                model = MarkovModel(f.read().decode('utf-8').split())
                await self.bot.db.markov.insert(tag, model.word_dict)
                self.markov_models[tag] = model
                await ctx.send(f"Tag `{tag}` has been created.")


def setup(bot):
    bot.add_cog(Other(bot))
