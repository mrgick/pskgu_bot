"""
    Файл с функциями-справками.
"""

from ..bot import simple_answer
from ..tools.messages import MSG_HELP, MSG_TIMETABLE, msg_start
from ..tools.filters import HELP_FILTER
from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent)

help_router = DefaultRouter()


@simple_bot_message_handler(help_router, HELP_FILTER.BEGIN)
@simple_answer
async def begin(event: SimpleBotEvent):
    """
        Выводит начальное сообщение пользователю.
    """
    user_id = event.object.object.message.from_id
    name = (await
            event.api_ctx.api_request("users.get",
                                      {"user_ids": user_id}))["response"][0]
    name = name['last_name'] + " " + name['first_name']
    return msg_start(name)


@simple_bot_message_handler(help_router, HELP_FILTER.HELP)
@simple_answer
async def help(event: SimpleBotEvent):
    """
        Выводит справку пользователю.
    """
    return MSG_HELP


@simple_bot_message_handler(help_router, HELP_FILTER.TIME_CLASSES)
@simple_answer
async def time_classes(event: SimpleBotEvent):
    """
        Выводит справку о времени начала пар.
    """
    return MSG_TIMETABLE
