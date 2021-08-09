"""
    Файл содержит все фильтры.
"""

from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent, TextFilter, CommandsFilter,
                         PayloadFilter)


class HELP_FILTER:
    """
        Фильтры help хендлера.
    """
    BEGIN = (TextFilter("начать") | TextFilter("start")
             | PayloadFilter({"command": "start"}))
    HELP = CommandsFilter(commands=("help", "справка"), prefixes=("/"))
    TIME_CLASSES = CommandsFilter(commands=("расписание_пар", "time_classes"),
                                  prefixes=("/"))


MAP_FILTER = CommandsFilter(commands=("map", "карта"), prefixes=("/"))


class SCHEDULE_FILTER:
    SHOW = CommandsFilter(commands=("show", "показать"), prefixes=("/"))
    FIND = CommandsFilter(commands=("find", "поиск"), prefixes=("/"))


class USER_SETTINGS:
    SUBSCRIBE = CommandsFilter(commands=("подписаться", "subscribe"),
                               prefixes=("/"))
    UNSUBCRIBE = CommandsFilter(commands=("отписаться", "unsubscribe"),
                                prefixes=("/"))
    DELETE = CommandsFilter(commands=("удалить", "delete"), prefixes=("/"))
