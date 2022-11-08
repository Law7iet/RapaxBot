import asyncio
from typing import Union

import requests
from disnake import ApplicationCommandInteraction, ModalInteraction
from disnake.utils import get

from constants import AuthorizationLevelEnum, authorizationLevel


# Some Functions
def check_data(url: str) -> dict | None:
    """
    Make an HTTP get request and check if the response is correct, checking the attribute 'status'

    Args:
        url: the url request.

    Returns:
        the url response. If the request is invalid, it return None.
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


async def check_role(inter: ApplicationCommandInteraction,
                     level: AuthorizationLevelEnum) -> bool:
    """
    Check if the sender has the correct role.
    It's use for authorization member to trigger bots command.

    Args:
        inter: the application command interation (context).
        level: it's the level of authorization.

    Returns:
        it represents if the member has the authorization.
    """
    for i in range(1, int(level) + 1):
        role = get(inter.guild.roles, id=authorizationLevel[i])
        if role in inter.author.roles:
            return True
    return False


async def send_response_and_clear(inter: Union[ApplicationCommandInteraction,
                                               ModalInteraction],
                                  defer: bool,
                                  text: str = "Done") -> None:
    if defer is True:
        await inter.send(text)
    else:
        await inter.response.send_message(text)
    await asyncio.sleep(5)
    message = await inter.original_message()
    await message.delete()
