from utils import exceptions
import constants


# TODO: create decorator checks where possible
def is_invoker_role_higher(ctx, member):
    if ctx.message.author.top_role <= member.top_role:
        raise exceptions.InvokerRoleTooLow


def is_bot_role_higher(ctx, member):
    if ctx.guild.me.top_role > member.top_role:
        return True
    else:
        return False


def is_bot_developer(ctx):
    if ctx.message.author.id not in constants.bot_developer_ids:
        raise exceptions.InvokerNotDeveloper
    else:
        return True
