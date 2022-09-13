from pskgu_bot.bots import messages
from pskgu_bot.db.services import (find_group_by_name, find_vk_user_by_id,
                                   update_user, delete_user)
from typing import Optional


async def subcribe(user_id: Optional[str] = None,
                   group_name: Optional[str] = None,
                   type_sys: str = "vk") -> str:
    """
        Подписывает пользователя на группу.
    """
    if group_name is None or user_id is None:
        return messages.MSG_NO_NAME_GROUP

    group = await find_group_by_name(group_name)
    if not group:
        return messages.msg_not_found_group_name(group_name)

    if type_sys == "vk":
        user = await find_vk_user_by_id(user_id)
        if user:
            if user.group == group_name:
                return messages.msg_already_subscribed(group_name)
        await update_user(user_id, group_name)
    return messages.msg_now_subscribed(group_name)


async def unsubcribe(user_id: Optional[str] = None,
                     type_sys: str = "vk") -> str:
    """
        Отписывает пользователя от группы.
    """
    if user_id is None:
        return messages.MSG_NO_USER_GROUP

    if type_sys == "vk":
        user = await find_vk_user_by_id(user_id)
        if not user:
            return messages.MSG_NO_USER_GROUP
        else:
            if user.group == "":
                return messages.MSG_NO_USER_GROUP
            else:
                await update_user(user_id, "")
    return messages.MSG_NOW_UNSUBCRIBE


async def delete(user_id: Optional[str] = None, 
                 type_sys: str = "vk") -> str:
    """
        Удаляет вк пользователя из бд.
    """
    if type_sys == "vk":
        user = await find_vk_user_by_id(user_id)
        if not user:
            return messages.MSG_USER_NOT_FOUND_IN_BD
        await delete_user(user_id)
    return messages.MSG_USER_DELETED_FROM_BD