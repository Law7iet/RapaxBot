import requests
from discord.utils import get
from discord.ext.commands.context import Context
from constants import AuthorizationLevelEnum, authorizationLevel

# Some Functions
def checkData(url: str) -> dict | None:
    """
    Make an HTTP get request and check if the response is correct, checking the attribute 'status'

    Args:
        `url` (str): the url request.

    Returns:
        `response`: the url response. If the request is invalid, it return None.
    """
    # send request
    reply = requests.get(url=url)
    data = reply.json()
    # check data errors
    if data['status'] != 'ok':
        print('Status error: ' + data['status'])
        return None
    else:
        return data

async def checkRole(ctx: Context, level: AuthorizationLevelEnum) -> bool:
    """
    Check if the sender has the correct role.
    It's use for authotization member to trigger bot's command.

    Args:
        `ctx` (Context): it's the context.
        `level` (AuthorizationLevelEnum): it's the level of authorization.

    Returns:
        `hasRole`: it represents if the member has the authorization.
    """    
    for i in range(1, int(level) + 1):
        role = get(ctx.guild.roles, id = authorizationLevel[i])
        if role in ctx.message.author.roles:
            return True
    await ctx.message.delete()
    await ctx.send(ctx.message.author.display_name + " non hai i permessi")
    return False