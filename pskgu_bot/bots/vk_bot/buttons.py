from asyncio.log import logger
from os import EX_CANTCREAT
from unittest import result
from vkbottle import Keyboard, KeyboardButtonColor, Text, EMPTY_KEYBOARD
from vkbottle.bot import BotLabeler, Message, rules
from pskgu_bot.bots import messages
from pskgu_bot.bots.base.shedule import show_schedule
from pskgu_bot.bots_old.vk_bot.bot import Startwith
from .bot import Contains_any, vk_get_message
from ..constants import button_commands, button_presets
from .. import base_io
import json

bl = BotLabeler()


@bl.message(Contains_any(button_commands))
async def keyboard_request(message: Message):
    """
        Запрос пользователя на добавление кнопок
    """
    user = await message.get_user()
    username = user.last_name + " " + user.first_name

    try:
        p_message = base_io.Parsed_message(message, username, from_ = 'vk', commands = button_commands)

        req_preset = p_message.next_str()

        if req_preset is None or req_preset in ['help', 'помощь', 'справка']:
            await p_message.cls_message.answer(message = messages.MSG_BUTTON_HELP)
            return

        if req_preset in ['delete', 'remove', 'удалить', 'убрать']:
            await p_message.cls_message.answer(message = messages.MSG_BUTTON_DELETE, keyboard = EMPTY_KEYBOARD)
            return

        if req_preset in ['custom', 'свои']:
            answer, keyboard = await set_custom_buttons_from(p_message)
            if keyboard is not None:
                await p_message.cls_message.answer(message = answer, keyboard = keyboard)
            else:
                await p_message.cls_message.answer(message = answer)
            return

        for preset in button_presets:
            if (req_preset in button_presets[preset]['keywords'] or
                req_preset in button_presets[preset].get('soft_keywords', [])
                ): 
                selected = button_presets[preset]
                break

        else:
            await p_message.cls_message.answer(message = messages.MSG_BUTTON_NO_SUCH_PRESET)
            return

        answer = messages.MSG_BUTTON_HELP
        keyboard = None

        if special:= selected.get('special', ''):
            match special:
                case 'special_shifted': 
                    answer = messages.MSG_BUTTON_SHOW_SHIFTED
                    keyboard = get_show_shifted_keyboard()
        
        else:
            answer = selected.get('on_select', messages.MSG_BUTTON_BASE)
            keyboard = make_keyboard(selected)

        if keyboard is not None:
            await p_message.cls_message.answer(message = answer, keyboard = keyboard)
        else:
            await p_message.cls_message.answer(message = messages.MSG_BUTTON_ERROR)

    except Exception as e:
        logger.error('Failed to make keyboard to user "{}":\n{}'.format(username, message.text))
        logger.error(e)
        await p_message.cls_message.answer(message = messages.MSG_BUTTON_ERROR)

def make_keyboard (preset: dict):
    keyboard = Keyboard(one_time=False, inline=False)

    for button in range(len(preset['buttons'])):
        if preset['buttons'][button] == 'row': keyboard.row()

        elif type(preset['buttons'][button]) is list:
            text, name, cmd = preset['buttons'][button]
            payload = {
                'command': name,
                'exec': cmd,
            }
            color = KeyboardButtonColor.PRIMARY

            keyboard.add(Text(text, payload = payload), color = color)

    return keyboard.get_json()


@bl.message(rules.PayloadContainsRule({"command": "const"}))
async def show_payload_handler(message: Message):
    payload = json.loads(message.payload)
    message.text = payload.get("exec")
    await vk_get_message(message)


@bl.message(rules.PayloadContainsRule({"command": "special_shifted"}))
async def show_payload_handler(message: Message):
    user_id = message.from_id
    payload = json.loads(message.payload)
    week = payload.get("week")

    mess, _ = await show_schedule(user_id=user_id,
                                  group_name=None,
                                  week_shift=week,
                                  image=False,
                                  type_sys="vk")

    #mess = messages.MSG_BUTTON_SHIFT + mess

    keyb = get_show_shifted_keyboard(week)

    await message.answer(message=mess, keyboard=keyb)


def get_show_shifted_keyboard(week: int = 0):
    keyboard = Keyboard(one_time=False, inline=False)

    keyboard.add(Text("Текущая неделя",
                      payload={
                          "command": "special_shifted",
                          "week": 0
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Предыдущая",
                      payload={
                          "command": "special_shifted",
                          "week": week - 1
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Следующая",
                      payload={
                          "command": "special_shifted",
                          "week": week + 1
                      }),
                 color=KeyboardButtonColor.PRIMARY)

    return keyboard.get_json()


@bl.message(rules.PayloadContainsRule({"command": "special_shifted_2"}))
async def show_payload_handler_2(message: Message):
    user_id = message.from_id
    payload = json.loads(message.payload)
    week = payload.get("week")

    mess, _ = await show_schedule(user_id=user_id,
                                  group_name=None,
                                  week_shift=week,
                                  image=False,
                                  type_sys="vk")

    #mess = messages.MSG_BUTTON_SHIFT + mess

    keyb = get_show_shifted_keyboard(week)

    await message.answer(message=mess, keyboard=keyb)


def get_show_shifted_2_keyboard(week: int = 0):
    keyboard = Keyboard(one_time=False, inline=False)

    match week:
        case -1: text = "Предыдущая неделя"
        case  0: text = "Текущая неделя"
        case  1: text = "Следующая неделя"

        case _ if week > 0: text = "Через " + str(week-1) + " недели(ю/ь)"
        case _ if week < 0: text = str(-week) + " недели(ю/ь) назад"

    keyboard.add(Text(text,
                      payload={
                          "command": "special_shifted",
                          "week": week
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    keyboard.row()
    keyboard.add(Text("Предыдущая",
                      payload={
                          "command": "special_shifted",
                          "week": week - 1
                      }),
                 color=KeyboardButtonColor.PRIMARY)
    keyboard.add(Text("Следующая",
                      payload={
                          "command": "special_shifted",
                          "week": week + 1
                      }),
                 color=KeyboardButtonColor.PRIMARY)

    return keyboard.get_json()




async def set_custom_buttons_from (message: base_io.Parsed_message) -> tuple | None:
    answer = 'Прогресс:\n'
    keyboard = Keyboard(one_time=False, inline=False)

    try:
        button = message.next_str()
        if button is None: return messages.MSG_BUTTON_CUSTOM, None

        while button:
            answer += button
            if button == 'row': 
                keyboard.row()
                answer += ' - успешно\n'

            else:
                result = button.replace('^', ' ').split(';')
                if len(result) >= 2:
                    text, cmd = result[:2]
                else: 
                    text = cmd = result[0]
                payload = {
                    'command': 'const',
                    'exec': cmd,
                }
                color = KeyboardButtonColor.PRIMARY

                answer += ' - текст "{}", команда "{}"'.format(text, cmd)
                keyboard.add(Text(text, payload = payload), color = color)
                answer += ' - успешно\n'

            button = message.next_str()

        return answer, keyboard.get_json()

    except Exception as e: 
        logger.error(e)
        answer += ' - провал\n'
        return answer, None