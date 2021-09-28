"""
    Файл с хендлерами поиска и вывода расписания.
"""

from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent, CommandsFilter, TextStartswithFilter)
from ..bot import simple_answer
from pskgu_bot.utils import str_to_int
from pskgu_bot.db.services import check_group
from pskgu_bot.bots.base.shedule import find_group, show_schedule

schedule_router = DefaultRouter()

SHOW = (CommandsFilter(commands=("show", "показать"), prefixes=("/"))
        | TextStartswithFilter(("show", "показать")))

FIND = (CommandsFilter(commands=("find", "поиск"), prefixes=("/"))
        | TextStartswithFilter(("find", "поиск")))


@simple_bot_message_handler(schedule_router, SHOW)
@simple_answer
async def show_schedule_handler(event: SimpleBotEvent):
    """
        Вывод расписания.
    """

    user_id = event.object.object.message.from_id
    args = event.object.object.message.text.split()[1:]

    group_name = None
    week_shift = None
    if len(args) > 0:
        if (await check_group(args[0]) is False
                and str_to_int(args[0]) is not None):
            week_shift = args[0]
        else:
            group_name = args[0]

    if len(args) > 1:
        if str_to_int(args[1]) is not None:
            week_shift = args[1]

    mess = await show_schedule(user_id, group_name, week_shift, "vk")
    return mess


@simple_bot_message_handler(schedule_router, FIND)
@simple_answer
async def find_group_handler(event: SimpleBotEvent):
    """
        Поиск имени группы.
    """
    args = event.object.object.message.text.split()[1:]
    if len(args) == 0:
        group_name = None
    else:
        group_name = str(args[0])
    mess = await find_group(group_name)
    return mess
