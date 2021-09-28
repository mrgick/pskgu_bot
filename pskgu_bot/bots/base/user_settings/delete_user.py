from ..messages import MSG_USER_NOT_FOUND_IN_BD, MSG_USER_DELETED_FROM_BD
from pskgu_bot.db.services import (find_vk_user_by_id, delete_user)
from typing import Optional


async def delete(user_id: Optional[str] = None, type_sys: str = "vk") -> str:
    """
        Удаляет вк пользователя из бд.
    """
    if type_sys == "vk":
        user = await find_vk_user_by_id(user_id)
        if not user:
            return MSG_USER_NOT_FOUND_IN_BD
        await delete_user(user_id)
    return MSG_USER_DELETED_FROM_BD
