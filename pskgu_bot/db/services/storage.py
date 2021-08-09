"""
    Файл с функциями взаимодействий с local_storage.
"""

from pskgu_bot.db.models import Group, Main_Page, Vk_User
from pskgu_bot.db import local_storage
from .group import find_all_groups
from vkwave.bots.storage.types import Key


async def initialize_storage():
    """
        Загрузка некоторых данных из бд в программу.
        (ensure_indexes требуется для работы umongo)
    """
    await Group.ensure_indexes()
    await Main_Page.ensure_indexes()
    await Vk_User.ensure_indexes()
    await local_storage.put(Key("groups"), await find_all_groups())
    await local_storage.put(Key("updated_groups"), [])
