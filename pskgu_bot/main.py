"""
    Запуск проекта (main-файл).
"""

import asyncio
from pskgu_bot.db.services import initialize_storage
from pskgu_bot.vk_bot.run import run_vk_bot
from pskgu_bot.parser.run import run_parser

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(initialize_storage())
    loop.create_task(run_vk_bot())
    loop.create_task(run_parser())
    loop.run_forever()
