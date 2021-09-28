"""
    Файл с функциями, отвечающими за карту и навигацию по ПГУ.
"""

from ..bot import vk_send_message
from ..tools.filters import MAP_FILTER
from vkwave.bots import (DefaultRouter, simple_bot_message_handler,
                         SimpleBotEvent)

map_router = DefaultRouter()

photos = ("photo-176090321_457239022,photo-176090321_457239021," +
          "photo-176090321_457239020,photo-176090321_457239019")


@simple_bot_message_handler(map_router, MAP_FILTER)
async def show_map(event: SimpleBotEvent):
    """
        Выводит карту зданий ПГУ на Льва Толстого 4.
    """
    peer_id = event.object.object.message.peer_id
    await vk_send_message(peer_id=peer_id, attachment=photos)
