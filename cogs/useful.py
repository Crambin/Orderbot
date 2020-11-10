import typing
import datetime
from googletrans import Translator

import discord
from discord.ext import commands
from discord import AllowedMentions

import utils
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
            settings = constants.lang_settings.copy()
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
            return await self.translate(ctx, query=query, timeout=timeout - 1, settings=settings)

        await ctx.send(text, allowed_mentions=AllowedMentions(everyone=False, roles=False))

    @commands.command(aliases=('del_bday, delete_birthday',))
    async def delbday(self, ctx, *, user: typing.Union[discord.Member, str] = None):
        """
        Deletes your birthday from the database.
        """
        if user is None:
            user = ctx.author
        elif ctx.author.id not in constants.bot_developer_ids \
                and str(user).lower() not in ("me", str(ctx.author).lower()):
            await ctx.send("You can only delete your own birthday from the database.")
            return
        elif isinstance(user, str):
            user = await utils.get_user_from_message(ctx, user)
            if user is None:
                await ctx.send("Please run the command again and specify which user you meant.")
                return

        current_record = await self.bot.db.user.fetch_birthday(user.id)
        if not current_record or current_record[0]['birthday'] is None:
            await ctx.send("Birthday is not stored in the database.")
            return

        # TODO: ask user for confirmation
        await self.bot.db.user.update_birthday(user.id, str(user), None)
        await ctx.send("Birthday has been successfully removed from the database.")

    # TODO: remove admin perms from adding users to db
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

    @staticmethod
    async def get_next_birthday_info(birthday):
        birth_year = birthday.year

        today = datetime.date.today()
        birthday = datetime.date(year=today.year, month=birthday.month, day=birthday.day)
        if birthday < today:
            birthday = datetime.date(year=today.year + 1, month=birthday.month, day=birthday.day)

        days_left = (birthday - today).days
        next_date = birthday.strftime("%d/%m/%Y")
        next_age = birthday.year - birth_year
        age_msg = str(next_age) + (
            "th" if 4 <= next_age % 100 <= 20 else {1: "st", 2: "nd", 3: "rd"}.get(next_age % 10, "th"))

        return days_left, next_date, age_msg

    async def get_ordered_birthdays(self, ctx):
        guild_member_ids = {member.id for member in ctx.guild.members}
        birthdays = await self.bot.db.user.fetch_all_birthdays()

        members = [user_record for user_record in birthdays if user_record['userid'] in guild_member_ids]
        num_birthdays = len(members)
        if num_birthdays == 0:
            return []

        index = 0
        today = datetime.date.today().isoformat().split('-', 1)[1]
        while index < num_birthdays and members[index]['birthday'].isoformat().split('-', 1)[1] < today:
            index += 1

        return members[index:] + members[:index]

    async def get_next_members_birthdays(self, ctx):
        ordered_birthdays = await self.get_ordered_birthdays(ctx)
        if not ordered_birthdays:
            return []

        next_birthdays = [ordered_birthdays[0]]
        first_birthday = next_birthdays[0]['birthday']
        for user_record in ordered_birthdays[1:]:
            birthday = user_record['birthday']
            if birthday.day == first_birthday.day and birthday.month == first_birthday.month:
                next_birthdays.append(birthday)
            else:
                break

        return next_birthdays

    @commands.command()
    @commands.guild_only()
    async def birthday(self, ctx, *, query=None):
        """
        Shows the birthday of a user.
        If no input is given, will show the birthday of the user whose birthday it is next.
        If an input is given, it will try to find that user and output their birthday.
        """
        if query is None:
            next_birthdays = await self.get_next_members_birthdays(ctx)
            if not next_birthdays:
                await ctx.send("There are no birthdays registered on this server.")
                return
        else:
            user = await utils.get_user_from_message(ctx, query)
            if user is None:
                await ctx.send("Please run the command again and specify which user you meant.")
                return

            birthday = await self.bot.db.user.fetch_birthday(user.id)
            if not birthday:
                await ctx.send(f"The user `{str(user)}` does not have a birthday stored in the database.")
                return
            next_birthdays = [(user.id, birthday[0]['birthday'])]

        # TODO: implement this embed to include the all birthdays formatting
        if len(next_birthdays) > 1:
            await ctx.send("Will implement this later")
            return

        user_id, birthday = next_birthdays[0]
        user = self.bot.get_user(user_id)

        # TODO: make this an embed
        days_left, next_date, age_msg = await self.get_next_birthday_info(birthday)
        if query is None:
            await ctx.send(f"The next birthday is on `{next_date}`.\n" 
                           f"This is {user}'s {age_msg} birthday, which is `{days_left}` days from now.")
        else:
            await ctx.send(f"{user}'s {age_msg} birthday is on {next_date}, which is `{days_left}` days from now.")


def setup(bot):
    bot.add_cog(Useful(bot))
