"""
    Файл с функциями, отвечающими за работу с пользовательскими настройками.
"""

from ..bot import simple_answer
from ..tools.filters import USER_SETTINGS
from ..tools.messages import (
    MSG_NO_NAME_GROUP,
    MSG_NOW_UNSUBCRIBE,
    MSG_USER_NOT_FOUND_IN_BD,
    MSG_USER_DELETED_FROM_BD,
    msg_not_found_group_name,
    msg_already_subscribed,
    msg_now_subscribed
)
from pskgu_bot.db.services import (find_group_by_name, find_vk_user_by_id,
                                   update_user, delete_user)
from vkwave.bots import (
    DefaultRouter,
    simple_bot_message_handler,
    SimpleBotEvent
)

user_settings_router = DefaultRouter()


@simple_bot_message_handler(user_settings_router, USER_SETTINGS.SUBSCRIBE)
@simple_answer
async def subcribe(event: SimpleBotEvent) -> str:
    """
        Подписывает вк пользователя на группу.
    """
    args = event.object.object.message.text.split()[1:]
    user_id = event.object.object.message.from_id

    if len(args) == 0:
        return MSG_NO_NAME_GROUP
    group_name = args[0]

    group = await find_group_by_name(group_name)
    if not group:
        return msg_not_found_group_name(group_name)

    user = await find_vk_user_by_id(user_id)
    if user:
        if user.group == group_name:
            return msg_already_subscribed(group_name)

    await update_user(user_id, group_name)
    return msg_now_subscribed(group_name)


@simple_bot_message_handler(user_settings_router, USER_SETTINGS.UNSUBCRIBE)
@simple_answer
async def unsubcribe(event: SimpleBotEvent) -> str:
    """
        Отписывает вк пользователя от группы.
    """
    user_id = event.object.object.message.from_id
    user = await find_vk_user_by_id(user_id)
    if not user:
        return MSG_NO_USER_GROUP
    await update_user(user_id, "")
    return MSG_NOW_UNSUBCRIBE


@simple_bot_message_handler(user_settings_router, USER_SETTINGS.DELETE)
@simple_answer
async def delete(event: SimpleBotEvent) -> str:
    """
        Удаляет вк пользователя из бд.
    """
    user_id = event.object.object.message.from_id
    user = await find_vk_user_by_id(user_id)
    if not user:
        return MSG_USER_NOT_FOUND_IN_BD
    await delete_user(user_id)
    return MSG_USER_DELETED_FROM_BD
