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


async def member_info(bot, member):
    roles = [role.mention for role in reversed(member.roles) if role.name != '@everyone']
    num_roles = len(roles)
    if num_roles > 50:
        roles = roles[:50]
        roles.append(f">>>> [50/{num_roles}] roles")

    roles = ', '.join(roles) or "**No roles**"
    server_join_time = member.joined_at.strftime("%d/%m/%Y @ %H:%M:%S")
    discord_join_time = member.created_at.strftime("%d/%m/%Y @ %H:%M:%S")

    user_record = await bot.db.user.fetch_birthday(member.id)
    if not user_record:
        birthday = None
    else:
        birthday = user_record[0]['birthday']

    embed = discord.Embed(description=discord.Embed.Empty, title=discord.Embed.Empty, colour=member.top_role.colour)
    embed.set_author(name=str(member), icon_url=member.avatar_url)
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='**ID**', value=f"{member.id}")
    embed.add_field(name='**Nickname**', value=member.nick)
    embed.add_field(name='**Birthday**', value=birthday, inline=False)
    embed.add_field(name=f'**Roles [{num_roles}]**', value=roles, inline=False)
    embed.add_field(name='**Account Created**', value=discord_join_time)
    embed.add_field(name='**Server Join Date**', value=server_join_time)

    return embed
