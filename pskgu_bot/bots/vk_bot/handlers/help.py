"""
    Файл с функциями-справками.
"""

from ..bot import simple_answer
from pskgu_bot.bots.base.help import begin, help, time_classes
from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent, TextFilter, PayloadFilter,
                         CommandsFilter, TextStartswithFilter)

BEGIN = (TextFilter("начать") | TextFilter("start")
         | PayloadFilter({"command": "start"}))
HELP = (CommandsFilter(commands=("help", "справка"), prefixes=("/"))
        | TextStartswithFilter(("help", "справка")))
TIME_CLASSES = (CommandsFilter(commands=("расписание_пар", "time_classes"),
                               prefixes=("/"))
                | TextStartswithFilter(("расписание_пар", "time_classes")))

help_router = DefaultRouter()


@simple_bot_message_handler(help_router, BEGIN)
@simple_answer
async def begin_handler(event: SimpleBotEvent):
    """
        Выводит начальное сообщение пользователю.
    """
    user_id = event.object.object.message.from_id
    name = (await
            event.api_ctx.api_request("users.get",
                                      {"user_ids": user_id}))["response"][0]
    name = name['last_name'] + " " + name['first_name']
    return begin(name)


@simple_bot_message_handler(help_router, HELP)
@simple_answer
async def help_handler(event: SimpleBotEvent):
    """
        Выводит справку пользователю.
    """
    return help()


@simple_bot_message_handler(help_router, TIME_CLASSES)
@simple_answer
async def time_classes_handler(event: SimpleBotEvent):
    """
        Выводит справку о времени начала пар.
    """
    return time_classes()
