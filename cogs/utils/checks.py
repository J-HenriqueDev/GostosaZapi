import discord
from discord.ext import commands


async def check_guild_permissions(ctx, perms, *, check=all):
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True

    if ctx.guild is None:
        return False

    resolved = ctx.author.guild_permissions
    return check(getattr(resolved, name, None) == value for name, value in perms.items())


def has_role(ctx, role):
    if ctx.channel is discord.DMChannel:
        return False

    role = discord.utils.get(ctx.author.roles, name=role)
    return role is not None


def has_guild_permissions(*, check=all, **perms):
    async def pred(ctx):
        return await check_guild_permissions(ctx, perms, check=check)
    return commands.check(pred)



def is_owner():
    def predicate(ctx):
        is_owner = (ctx.message.author.id ==[431141741194641408,515903666360942594])
        return is_owner
    return commands.check(predicate)


def is_admin():
    async def pred(ctx):
        return await check_guild_permissions(ctx, {'administrator': True})
    return commands.check(pred)


