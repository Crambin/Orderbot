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
