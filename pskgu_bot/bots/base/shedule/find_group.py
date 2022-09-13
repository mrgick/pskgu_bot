from pskgu_bot.db.services import find_groups_name
from pskgu_bot.bots import messages
from typing import Optional


async def find_group(group_name: Optional[str] = None) -> str:
    """
        Поиск имени группы.
    """

    if group_name == "" or group_name is None:
        return messages.MSG_NO_NAME_GROUP

    groups = await find_groups_name(group_name)
    if groups == []:
        return messages.MSG_GROUPS_IN_BD_NOT_FOUND

    mess = ""
    for x in groups:
        mess += x
        mess += "\n"
        if (len(mess)) >= 500:
            mess += "Всего записей: " + str(len(groups)) + "\n"
            break

    return messages.MSG_GROUPS_IN_BD_FOUND + mess


async def try_guess_user_group(group_name: str) -> str:
    if type(group_name) is not str or group_name == '': return ''

    groups = await find_groups_name(group_name[1:4])
    if len(groups) == 0: return messages.msg_not_found_group_name(group_name)
    else: return messages.msg_found_something(groups)