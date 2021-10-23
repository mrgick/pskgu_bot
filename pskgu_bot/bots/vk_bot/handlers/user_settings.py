"""
    Файл с функциями, отвечающими за работу с пользовательскими настройками.
"""

from ..bot import Startwith
from vkbottle.bot import BotLabeler, Message
from pskgu_bot.bots.base.user_settings import subcribe, unsubcribe, delete
from pskgu_bot.bots.base.services import get_first_arg

bl = BotLabeler()

SUBSCRIBE = (Startwith(("подписаться", "subscribe")))
UNSUBCRIBE = (Startwith(("отписаться", "unsubscribe")))
DELETE = (Startwith(("удалить", "delete")))


@bl.message(SUBSCRIBE)
async def subcribe_handler(message: Message) -> str:
    """
        Подписывает вк пользователя на группу.
    """
    args = message.text.split()[1:]
    user_id = message.from_id
    group_name = get_first_arg(args)
    return await subcribe(user_id, group_name, "vk")


@bl.message(UNSUBCRIBE)
async def unsubcribe_handler(message: Message) -> str:
    """
        Отписывает вк пользователя от группы.
    """
    user_id = message.from_id
    return await unsubcribe(user_id, "vk")


@bl.message(DELETE)
async def delete_handler(message: Message) -> str:
    """
        Удаляет вк пользователя из бд.
    """
    user_id = message.from_id
    return await delete(user_id, "vk")
