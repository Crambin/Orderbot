from .helper import get_next_birthday_info

import discord


def infraction(member, infraction_type, reason, duration=0, dm=False):
    title = "**Infraction Information**"
    description = (f"**USER:** {member}\n"
                   f"**TYPE:** {infraction_type}\n"
                   f"**REASON:** {reason}")
    if duration:
        description += f"\n**DURATION:** {duration}"
    if dm:
        description += ("\nIf you believe this to have happened by mistake,\n"
                        "please contact a member of this server's staff to appeal.")

    return discord.Embed(title=title, description=description, colour=discord.Colour.dark_red())


async def birthdays(bot, next_birthdays):
    embed = discord.Embed(title="All Birthdays", color=discord.Colour.dark_gold())

    for user_record in next_birthdays:
        user_id, birthday = tuple(user_record)
        user = bot.get_user(user_id)
        days_left, next_date, age_msg = await get_next_birthday_info(birthday)
        embed.add_field(name="**{}** | {} Birthday".format(user.name, age_msg),
                        value="{} | `{} days` | `{}`".format(user.mention, days_left, next_date), inline=False)

        return embed
