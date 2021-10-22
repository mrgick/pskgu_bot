from pskgu_bot.db.services import find_group_by_name, find_vk_user_by_id
from pskgu_bot.utils.additions import str_to_int
from ..messages import (MSG_NO_NAME_GROUP, MSG_NO_USER_GROUP,
                        msg_not_found_group_name)
from typing import Optional


async def get_group_url(user_id: Optional[str] = None,
                        group_name: Optional[str] = None,
                        type_sys: str = "vk") -> str:
    """
        Выводит ссылку на расписание группы.
    """

    if (group_name is None or group_name == ""):
        group_name = None

    user_id = str_to_int(user_id)

    if (user_id is not None and group_name is None and type_sys == "vk"):
        user = await find_vk_user_by_id(user_id)
        if user:
            group_name = user.group

    if (group_name is None or group_name == ""):
        return MSG_NO_NAME_GROUP

    group = await find_group_by_name(group_name)
    if group is None:
        return msg_not_found_group_name(group_name)
    else:
        return "Ссылка: " + group.page_url + "\n"
