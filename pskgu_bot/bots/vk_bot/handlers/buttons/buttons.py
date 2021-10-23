from ...bot import Startwith
from .keyboards import get_show_keyboard, get_show_shifted_keyboard
from pskgu_bot.bots.base.buttons.messages import (SHOW_MESSAGE, DELETE_MESSAGE,
                                                  HELP_MESSAGE,
                                                  SHOW_SHIFTED_MESSAGE)
from pskgu_bot.bots.base.services import get_first_arg
from pskgu_bot.bots.base.shedule import show_schedule
from vkbottle import EMPTY_KEYBOARD
from vkbottle.bot import BotLabeler, Message, rules
import json

bl = BotLabeler()


@bl.message(rules.PayloadContainsRule({"command": "show"}))
async def show_payload_handler(message: Message):

    user_id = message.from_id
    payload = json.loads(message.payload)
    week = payload.get("week")
    mess, _ = await show_schedule(user_id=user_id,
                                  group_name=None,
                                  week_shift=week,
                                  image=False,
                                  type_sys="vk")
    keyb = get_show_shifted_keyboard(week)
    await message.answer(message=mess, keyboard=keyb)


@bl.message(Startwith(("buttons", "кнопки")))
async def buttons(message: Message):
    """
        Выводит кнопки.
    """
    args = message.text.split(" ")[1:]
    elem = get_first_arg(args)
    if elem == "help":
        return HELP_MESSAGE
    elif elem == "show":
        mess = SHOW_MESSAGE
        keyb = get_show_keyboard()
    elif elem == "show_shifted":
        mess = SHOW_SHIFTED_MESSAGE
        keyb = get_show_shifted_keyboard(week=0)
    elif elem == "delete":
        mess = DELETE_MESSAGE
        keyb = EMPTY_KEYBOARD
    else:
        return HELP_MESSAGE

    await message.answer(message=mess, keyboard=keyb)
