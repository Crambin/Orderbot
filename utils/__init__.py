from . import checks
from . import embed
from . import exceptions


async def get_user_from_message(ctx, query):
    if len(ctx.message.mentions) != 0:
        return ctx.message.mentions[0]

    query = query.lower()
    if query.startswith("me"):
        return ctx.message.author

    members_found = []
    for member in ctx.message.guild.members:
        if str(member) in query or str(member.id) in query:
            return member

        elif query in member.name.lower() or query in member.display_name.lower():
            members_found.append(member)

    if len(members_found) == 0:
        await ctx.send("No members were found by that name.")
    elif len(members_found) == 1:
        return members_found[0]
    else:
        await ctx.send(f"Multiple users found: {', '.join(str(member) for member in members_found)}")
        return None
