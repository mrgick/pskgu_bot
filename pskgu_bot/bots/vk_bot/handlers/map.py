"""
    Файл с функциями, отвечающими за карту и навигацию по ПГУ.
"""

from ..bot import Startwith
from vkbottle.bot import BotLabeler, Message
from pskgu_bot.bots.base.map import PHOTOS

bl = BotLabeler()

MAP_FILTER = (Startwith(("map", "карта")))


@bl.message(MAP_FILTER)
async def show_map(message: Message):
    """
        Выводит карту зданий ПГУ на Льва Толстого 4.
    """
    await message.answer(attachment=PHOTOS)
