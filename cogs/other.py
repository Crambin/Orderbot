import random
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
                                   f"API latency is {self.bot.latency*1000:.0f}ms")

    @commands.command()
    async def tags(self, ctx):
        tags = '`, `'.join(await self.bot.db.markov.get_tags())
        await ctx.send(f"Current tags: \n`{tags}`")

    @commands.command()
    async def markov(self, ctx, *, name):
        name = name.lower()
        if name in self.markov_models:
            model = self.markov_models.get(name, None)
        else:
            pairs = await self.bot.db.markov.fetch(name)
            model = MarkovModel(word_pairs=pairs) if pairs else None

        if model is None:
            await ctx.send("This tag does not exist within the markov database.")
            await self.tags(ctx)
            return

        self.markov_models[name] = model
        await ctx.send(model.generate())


def setup(bot):
    bot.add_cog(Other(bot))
