"""
    Файл с функциями, отвечающими за работу с пользовательскими настройками.
"""

from ..bot import simple_answer
from pskgu_bot.bots.base.user_settings import subcribe, unsubcribe, delete
from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent, CommandsFilter, TextStartswithFilter)

user_settings_router = DefaultRouter()

SUBSCRIBE = (CommandsFilter(commands=("подписаться", "subscribe"),
                            prefixes=("/")) | TextStartswithFilter(
                                ("подписаться", "subscribe")))
UNSUBCRIBE = (CommandsFilter(commands=("отписаться", "unsubscribe"),
                             prefixes=("/")) | TextStartswithFilter(
                                 ("отписаться", "unsubscribe")))
DELETE = (CommandsFilter(commands=("удалить", "delete"), prefixes=("/"))
          | TextStartswithFilter(("удалить", "delete")))


@simple_bot_message_handler(user_settings_router, SUBSCRIBE)
@simple_answer
async def subcribe_handler(event: SimpleBotEvent) -> str:
    """
        Подписывает вк пользователя на группу.
    """
    args = event.object.object.message.text.split()[1:]
    user_id = event.object.object.message.from_id
    group_name = None
    if len(args) > 0:
        group_name = args[0]
    return await subcribe(user_id, group_name, "vk")


@simple_bot_message_handler(user_settings_router, UNSUBCRIBE)
@simple_answer
async def unsubcribe_handler(event: SimpleBotEvent) -> str:
    """
        Отписывает вк пользователя от группы.
    """
    user_id = event.object.object.message.from_id
    return await unsubcribe(user_id, "vk")


@simple_bot_message_handler(user_settings_router, DELETE)
@simple_answer
async def delete_handler(event: SimpleBotEvent) -> str:
    """
        Удаляет вк пользователя из бд.
    """
    user_id = event.object.object.message.from_id
    return await delete(user_id, "vk")
