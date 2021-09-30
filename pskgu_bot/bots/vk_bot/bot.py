"""
    Вк бот
"""

from vkbottle.bot import Bot, Message, rules
from pskgu_bot import Config
from pskgu_bot.utils import logger


class Startwith(rules.ABCMessageRule):
    def __init__(self, words: tuple):
        self.words = words

    async def check(self, message: Message) -> bool:
        message.text = message.text.replace("[club176090321|@mrgick]", "")
        message.text = message.text.replace("  ", " ")

        if message.text.startswith(" "):
            message.text = message.text[1:]

        mess = message.text.split(" ")[0].lower()

        if mess.startswith("/"):
            mess = mess[1:]

        for word in self.words:
            if word == mess:
                return True
        return False


async def vk_send_message(**kwargs):
    """
        Отправка сообщения в вк пользователю (user_id) или беседе (peer_id).
    """

    try:
        await vk_bot.api.messages.send(**kwargs, random_id=0)
    except Exception as e:
        logger.error(e)


# инициализация вк бота
vk_bot = Bot(token=Config.VK_TOKEN)
