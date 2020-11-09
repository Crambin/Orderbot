import datetime
from discord.ext import commands
from discord import AllowedMentions
from googletrans import Translator

import constants


class Useful(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 2, commands.BucketType.member)
    async def translate(self, ctx, *, query=None, timeout=10, settings=None):
        """
        A google translate API.
        -s (source language) and -d (destination language) are optional arguments
        which may be added to the command to translate between selected languages.
        """
        if timeout == 0:
            await ctx.send("The google API has timed out; please try again.")
            return

        if settings is None or settings == constants.lang_settings:
            settings = constants.lang_settings
            for option in settings:
                pos = query.find(option)
                if pos != -1:
                    setting = query[pos + 3:].split(" ")[0]
                    settings[option] = setting

                    query = query[:pos] + query[pos + len(setting) + 4:]

        try:
            translated = Translator().translate(query, src=settings['-s'], dest=settings['-d'])

            src = constants.lang_codes[translated.src]
            dest = constants.lang_codes[translated.dest]

            text = "[{0} -> {1}] {2.text}".format(src, dest, translated)
        except ValueError:
            text = "Language could not be found."
        except AttributeError:
            return await self.translate(ctx, query=query, timeout=timeout-1, settings=settings)

        await ctx.send(text, allowed_mentions=AllowedMentions(everyone=False, roles=False))

    @commands.command(aliases=('set_birthday', 'set_bday'))
    @commands.guild_only()
    async def setbday(self, ctx, *, query=None):
        """
        Sets your birthday into the database in form `DD/MM/YYYY`.
        Usage: `!setbday DD/MM/YYYY`.
        """
        if query is None:
            await ctx.send("Usage: `!setbday DD/MM/YYYY`.")
            return
        elif len(ctx.message.mentions) > 1:
            await ctx.send("I can only set the birthday of one user at a time.")
            return

        if ctx.message.mentions and ctx.message.author.guild_permissions.administrator:
            user = ctx.message.mentions[0]
            query = query.split("> ")[1]
        elif ctx.message.mentions:
            await ctx.send("You can only set your own birthday if you are not an administrator.")
            return
        else:
            user = ctx.message.author

        try:
            dob = datetime.datetime.strptime(query, "%d/%m/%Y").date()
        except ValueError:
            await ctx.send("Invalid date.\nDate must be written as `DD/MM/YYYY`.")
            return

        if not 1900 <= dob.year <= 2020:
            await ctx.send("Nice try. Birth year must be between 1900 and 2020.")
            return

        await self.bot.db.user.update_birthday(user.id, str(user), dob)
        await ctx.send(f"Birthday set successfully for {str(user)}.")


def setup(bot):
    bot.add_cog(Useful(bot))
