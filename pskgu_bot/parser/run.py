"""
    Запускает парсер и отправляет уведомление об изменении пользователю
"""

from .parser import (get_page, get_hash, start_parser)
from pskgu_bot.db.services import (initialize_storage, get_main_page_hash,
                                   set_main_page_hash, update_info_main_page,
                                   create_structured_rasp,
                                   set_main_page_structure)
from pskgu_bot import Config
from pskgu_bot.utils import logger
from pskgu_bot.bots.vk_bot.update import send_updates_to_users
from asyncio import sleep


async def run_parser():
    """
        Запуск цикла парсера.
    """
    while True:
        try:
            sleeping_time = 60
            hash_now = get_hash(await get_page(Config.REMOTE_URL))
        except Exception:
            sleeping_time = 1800
            logger.error("Can't get hash of main_page")
        else:
            hash_in_db = await get_main_page_hash()
            if hash_in_db != hash_now:
                await start_parser()
                logger.info("Parsing DONE")
                await set_main_page_hash(hash_now)
                structure = await create_structured_rasp()
                await set_main_page_structure(structure)
                upd_groups = await update_info_main_page()
                await initialize_storage()
                await send_updates_to_users(upd_groups)
        finally:
            await sleep(sleeping_time)
