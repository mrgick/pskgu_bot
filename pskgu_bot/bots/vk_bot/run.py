"""
    Файл запуска вк бота.
"""

from .bot import vk_bot
from .handlers import (help_router, schedule_router, map_router,
                       user_settings_router)

# добавляем handlers к боту
vk_bot.dispatcher.add_router(user_settings_router)
vk_bot.dispatcher.add_router(schedule_router)
vk_bot.dispatcher.add_router(map_router)
vk_bot.dispatcher.add_router(help_router)


async def run_vk_bot():
    """
        Запуск вк бота.
    """
    await vk_bot.run(ignore_errors=True)
