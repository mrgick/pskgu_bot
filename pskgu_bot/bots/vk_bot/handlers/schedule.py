"""
    Файл с хендлерами поиска и вывода расписания.
"""

from ..bot import Startwith, vk_bot
from pskgu_bot.utils import str_to_int
from pskgu_bot.db.services import check_group
from pskgu_bot.bots.base.shedule import find_group, show_schedule
from vkbottle.bot import BotLabeler, Message
from vkbottle.tools import PhotoMessageUploader
from io import BytesIO
import json

bl = BotLabeler()

SHOW = (Startwith(("show", "показать")))
FIND = (Startwith(("find", "поиск")))


@bl.message(SHOW)
async def show_schedule_handler(message: Message):
    """
        Вывод расписания.
    """

    user_id = message.from_id
    args = message.text.split(" ")[1:]

    group_name = None
    week_shift = None
    image = False

    if "img" in args:
        image = True
        args.remove("img")

    if len(args) > 0:
        if (await check_group(args[0]) is False
                and str_to_int(args[0]) is not None):
            week_shift = args[0]
        else:
            group_name = args[0]

    if len(args) > 1:
        if str_to_int(args[1]) is not None:
            week_shift = args[1]

    mess, img = await show_schedule(user_id, group_name, week_shift, image,
                                    "vk")
    if img:
        photo = await PhotoMessageUploader(vk_bot.api).upload(img)
        await message.answer(attachment=photo)
    else:
        return mess


@bl.message(FIND)
async def find_group_handler(message: Message) -> str:
    """
        Поиск имени группы.
    """
    args = message.text.split()[1:]
    if len(args) == 0:
        group_name = None
    else:
        group_name = str(args[0])
    mess = await find_group(group_name)
    return mess
