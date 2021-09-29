from pskgu_bot.db.services import find_groups_name
from ..messages import (MSG_GROUPS_IN_BD_FOUND, MSG_GROUPS_IN_BD_NOT_FOUND,
                        MSG_NO_NAME_GROUP)
from typing import Optional


async def find_group(group_name: Optional[str] = None) -> str:
    """
        Поиск имени группы.
    """

    if group_name == "" or group_name is None:
        return MSG_NO_NAME_GROUP

    groups = await find_groups_name(group_name)
    if groups == []:
        return MSG_GROUPS_IN_BD_NOT_FOUND

    mess = ""
    for x in groups:
        mess += x
        mess += "\n"
        if (len(mess)) >= 500:
            mess += "Всего записей: " + str(len(groups)) + "\n"
            break

    return MSG_GROUPS_IN_BD_FOUND + mess
