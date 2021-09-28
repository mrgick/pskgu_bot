"""
    Файл с функциями, отвечающими за карту и навигацию по ПГУ.
"""

from ..bot import vk_send_message
from pskgu_bot.bots.base.map import PHOTOS
from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent, CommandsFilter, TextStartswithFilter)

map_router = DefaultRouter()

MAP_FILTER = (CommandsFilter(commands=("map", "карта"), prefixes=("/"))
              | TextStartswithFilter(("map", "карта")))


@simple_bot_message_handler(map_router, MAP_FILTER)
async def show_map(event: SimpleBotEvent):
    """
        Выводит карту зданий ПГУ на Льва Толстого 4.
    """
    peer_id = event.object.object.message.peer_id
    await vk_send_message(peer_id=peer_id, attachment=PHOTOS)
