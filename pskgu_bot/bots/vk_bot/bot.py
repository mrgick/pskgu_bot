"""
    Вк бот
"""

from vkbottle.bot import BotLabeler, Bot, Message, rules
from pskgu_bot import Config
from pskgu_bot.utils import logger
from ..constants import available_commands
from .. import base_io

# initialization
vk_bot = Bot(token=Config.VK_TOKEN)
bl = BotLabeler()

# other

class Contains_any(rules.ABCMessageRule):
    def __init__(self, commands: dict):
        self.commands = commands

    async def check(self, message: Message) -> bool:
        text = message.text.lower()

        if text.startswith("/"):
            text = text[1:]

        for cmd in self.commands:
            for keyword in self.commands[cmd]['keywords']:
                if text.startswith(keyword): return True

        for cmd in self.commands:
            for keyword in self.commands[cmd]['keywords']:
                if keyword in text: return True

        for cmd in self.commands:
            for keyword in self.commands[cmd].get('soft_keywords', []):
                if text.startswith(keyword): return True

        for cmd in self.commands:
            for keyword in self.commands[cmd].get('soft_keywords', []):
                if keyword in text: return True

        return False

@bl.message(Contains_any(available_commands))
async def vk_get_message(message: Message):
    """
        Get message from vk-user
    """

    user = await message.get_user()
    username = user.last_name + " " + user.first_name

    p_message = base_io.Parsed_message(message, username, from_ = 'vk')

    answer = await base_io.input_message(p_message)
    
    if answer: 
        await vk_send_message(user_id = message.from_id, message = answer)


async def vk_send_message(**kwargs):
    """
        Send message to vk-user (user_id) or vk group chat (peer_id).
    """

    try:
        await vk_bot.api.messages.send(**kwargs, random_id=0)
    except Exception as e:
        logger.error(e)

    #await message.answer(attachment=PHOTOS)