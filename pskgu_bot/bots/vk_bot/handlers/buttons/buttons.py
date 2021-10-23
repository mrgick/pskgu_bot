from ...bot import Startwith
from .keyboards import SHOW_BUTTONS_KEYBOARD
from pskgu_bot.bots.base.buttons.messages import (SHOW_MESSAGE, DELETE_MESSAGE,
                                                  HELP_MESSAGE)
from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import BotLabeler, Message
from pskgu_bot.bots.base.services import get_first_arg

bl = BotLabeler()


@bl.message(Startwith(("buttons", "кнопки")))
async def buttons(message: Message):
    """
        Выводит кнопки.
    """
    args = message.text.split(" ")[1:]
    elem = get_first_arg(args)
    if elem == "help" or elem is None:
        mess = HELP_MESSAGE
        return mess
    elif elem == "show":
        mess = SHOW_MESSAGE
        keyb = SHOW_BUTTONS_KEYBOARD
    elif elem == "delete":
        mess = DELETE_MESSAGE
        keyb = EMPTY_KEYBOARD

    await message.answer(message=mess, keyboard=keyb)
