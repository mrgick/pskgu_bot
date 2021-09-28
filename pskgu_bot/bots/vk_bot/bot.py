"""
    Вк бот
"""

from vkwave.bots import SimpleLongPollBot, SimpleBotEvent
from pskgu_bot import Config
from pskgu_bot.utils import logger


def simple_answer(func):
    """
        Простой декоратор для ответа на сообщение.
        (сделан для более лучшей читаемости кода)
    """
    async def wrapper(event: SimpleBotEvent):
        message = await func(event)
        if message == "" or message is None:
            message = ("Произошла неопознанная ошибка," +
                       " свяжитесь с администратором.")
        await event.answer(message=message)
    return wrapper


async def vk_send_message(**kwargs):
    """
        Отправка сообщения в вк пользователю (user_id) или беседе (peer_id).
    """
    try:
        await vk_bot.api_context.messages.send(**kwargs, random_id=0)
    except Exception as e:
        logger.error(e)

# инициализация вк бота
vk_bot = SimpleLongPollBot(tokens=Config.VK_TOKEN, group_id=Config.GROUP_ID)
