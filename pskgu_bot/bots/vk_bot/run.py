"""
    Файл запуска вк бота.
"""

from .bot import vk_bot, bl
from . import buttons

labelers = [buttons.bl, bl]


async def run_vk_bot():
    """
        Запуск вк бота.
    """
    for custom_labeler in labelers:
        vk_bot.labeler.load(custom_labeler)
    await vk_bot.run_polling()
