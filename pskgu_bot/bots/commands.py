"""
    Файл с командами бота.
"""

from multiprocessing.connection import wait
from pskgu_bot.db.services.group import check_group
from .constants import available_commands
from . import messages
from .base_io import Parsed_message

from pskgu_bot.db.services import find_vk_user_by_id
from pskgu_bot.bots.base.shedule import find_group, try_guess_user_group, show_schedule, get_group_url
from pskgu_bot.bots.base.subscribtion import subcribe, unsubcribe, delete
from vkbottle.tools import PhotoMessageUploader


def link_to_command (cmd_name): # добавляет функцию в список доступных команд
    def wrapper (func):
        available_commands[cmd_name]['func'] = func
        return func
    return wrapper



@link_to_command('begin')
async def CMD_begin (message: Parsed_message) -> str:
    """
        Выводит начальное сообщение пользователю.
    """
    return messages.MSG_START.format(username = message.username)


@link_to_command('help')
async def CMD_help (message: Parsed_message) -> str:
    """
        Выводит справку пользователю.
    """
    keyword = message.next_str()

    if keyword is None: return messages.MSG_HELP

    else:
        if keyword.startswith('/'): keyword = keyword[1:]

        for cmd in available_commands:
            if (keyword in available_commands[cmd]['keywords'] or
                keyword in available_commands[cmd].get('soft_keywords', [])
                ):
                return available_commands[cmd].get('on_help', messages.MSG_NO_HELP_AVAILABLE.format(cmd = keyword))

        else: return messages.MSG_INVALID_COMMAND.format(cmd = keyword)


@link_to_command('timetable')
async def CMD_timetable (message: Parsed_message) -> str:
    """
        Выводит справку пользователю.
    """
    return messages.MSG_TIMETABLE


@link_to_command('map')
async def CMD_map (message: Parsed_message) -> str:
    """
        Выводит карту зданий ПГУ на Льва Толстого 4.
    """
    await message.cls_message.answer(attachment = available_commands['map']['photos'])
    return ''


@link_to_command('show')
async def CMD_show (message: Parsed_message) -> str:
    """
        Вывод расписания.
    """

    with_image = (['img', 'image', 'фото'] in message)

    group_name = await message.try_find_group()

    if group_name is None:
        return messages.MSG_NO_NAME_GROUP
    elif not await check_group(group_name):
        return await try_guess_user_group(group_name)

    week_shift = (message.next_int() or 0)

    message, img = await show_schedule(message.from_id, 
                                       group_name, 
                                       week_shift, 
                                       with_image,
                                       message.from_)

    if img and message.from_ == 'vk': # не работает из-за внутренней ошибки show_schedule
        from vk_bot.bot import vk_bot
        photo = await PhotoMessageUploader(vk_bot.api).upload(img)
        await message.answer(attachment=photo)

    return message


@link_to_command('find')
async def CMD_find (message: Parsed_message) -> str:
    """
        Поиск имени группы.
    """
    return await find_group(message.next_str())


@link_to_command('url')
async def CMD_url (message: Parsed_message) -> str:
    """
        Вывод ссылки на расписание.
    """

    group_name = await message.try_find_group()

    if group_name is None:
        return messages.MSG_NO_NAME_GROUP
    elif not await check_group(group_name):
        return await try_guess_user_group(group_name)

    return await get_group_url(message.from_id, group_name, message.from_)


@link_to_command('subscribe')
async def CMD_subscribe (message: Parsed_message) -> str:
    """
        Позволяет пользователю подписаться на группу, либо узнать текущую подписку.
    """
    group_name = message.next_str()
    if group_name is None:
        value = str(message.next_int())
        if value and await check_group(value): group_name = value

    if group_name is None: # если нет параметра - вывести текущую подписку
        user = await find_vk_user_by_id(message.from_id)

        if user and user.group: # если подписка есть
            return messages.MSG_CURRENT_GROUP.format(group = user.group)
        else: # если подписки нет
            return messages.MSG_NO_CURRENT_GROUP

    else: return await subcribe(message.from_id, group_name, message.from_)


@link_to_command('unsubscribe')
async def CMD_unsubscribe (message: Parsed_message) -> str:
    """
        Отписывает вк пользователя от группы.
    """
    return await unsubcribe(message.from_id, message.from_)


@link_to_command('delete')
async def CMD_delete (message: Parsed_message) -> str:
    """
        Удаляет вк пользователя из бд.
    """
    return await delete(message.from_id, message.from_)