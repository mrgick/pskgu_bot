"""
    Файл с функциями-справками.
"""

from pskgu_bot.bots.base.help import begin, help, time_classes
from vkbottle.bot import BotLabeler, Message, rules
from ..bot import Startwith, vk_bot

BEGIN = (Startwith(("start", "начать"))
         or rules.PayloadRule({"command": "start"}))
HELP = Startwith(("help", "справка"))
TIME_CLASSES = (Startwith(("classes_time", "расписание_пар")))

bl = BotLabeler()


@bl.message(BEGIN)
async def begin_handler(message: Message) -> str:
    """
        Выводит начальное сообщение пользователю.
    """
    user = await message.get_user()
    name = user.last_name + " " + user.first_name
    return begin(name)


@bl.message(HELP)
async def help_handler(message: Message) -> str:
    """
        Выводит справку пользователю.
    """
    return help()


@bl.message(TIME_CLASSES)
async def time_classes_handler(message: Message) -> str:
    """
        Выводит справку о времени начала пар.
    """
    return time_classes()
