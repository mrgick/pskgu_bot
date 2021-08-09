"""
    Файл с функциями, отвечающими за поиск и вывод расписания.
"""

from ..bot import simple_answer
from ..tools.filters import SCHEDULE_FILTER
from ..tools.messages import (MSG_NO_USER_GROUP, MSG_NO_NAME_GROUP,
                              MSG_GROUPS_IN_BD_FOUND,
                              MSG_GROUPS_IN_BD_NOT_FOUND,
                              msg_not_found_group_name)

from pskgu_bot.db.services import (find_vk_user_by_id, find_group_by_name,
                                   find_groups_name, is_vk_user_subscribed)
from pskgu_bot.utils import get_week_days, get_name_of_day, translate_message
from vkwave.bots import (
    DefaultRouter,
    simple_bot_message_handler,
    SimpleBotEvent,
)

schedule_router = DefaultRouter()


@simple_bot_message_handler(schedule_router, SCHEDULE_FILTER.SHOW)
@simple_answer
async def show_schedule(event: SimpleBotEvent):
    """
        Выводит расписание.
    """
    def make_readable_text(group, keys):
        """
            Преобразуем group.days в читаемое сообщение.
        """
        mess = ""
        for key in keys:
            day = group.days.get(key)
            if day:
                day_name = get_name_of_day(key)
                mess += day_name + ", " + key + "\n"
                for x, lesson in day.items():
                    mess += x + ") " + lesson + "\n"
                mess += "\n"
        if mess == "":
            mess = "Данная неделя пуста.\n"
        return mess

    def str_to_int(x):
        """
            Перевод строки в число.
        """
        try:
            x = int(x)
            return x
        except Exception:
            return 0

    def get_week_message(args, group):
        """
            Вспомогательная функция.
            Возвращает сообщение об расписании.
        """
        def add_name(mess, group):
            """
                Вставка имени преподавателя или названия группы.
            """
            if group.prefix[0] == "преподователь":
                mess += "Преподователь: "
            else:
                mess += "Группа: "
            mess += group.name + "\n"
            return mess

        def add_url(mess, url, index):
            """
                Вставка ссылки в сообщение.
            """
            return mess[:(index + 1)] + url + mess[index:]

        mess = ""
        n = 0
        if len(args) > 0:
            n = str_to_int(args[0])

        keys = get_week_days(n)
        mess = add_name(mess, group)
        place_for_url = mess.index(mess[-1])
        mess += make_readable_text(group, keys)

        if len(args) > 1:
            mess += "\nСсылка:"
            mess = translate_message(mess, args[1])
            mess += " " + group.page_url + "\n"
        else:
            url = "Ссылка: " + group.page_url + "\n"
            mess = add_url(mess, url, place_for_url)
        return mess

    args = event.object.object.message.text.split()[1:]
    user_id = event.object.object.message.from_id
    user = await find_vk_user_by_id(user_id)
    group_name = ""

    if user:
        group_name = user.group

    if len(args) > 0:
        if str_to_int(args[0]) == 0 and args[0] != "0":
            group_name = args[0]
            args = args[1:]

    if group_name == "":
        return MSG_NO_NAME_GROUP

    group = await find_group_by_name(group_name)
    if not group:
        return msg_not_found_group_name(group_name)
    return get_week_message(args, group)


@simple_bot_message_handler(schedule_router, SCHEDULE_FILTER.FIND)
@simple_answer
async def find_group(event: SimpleBotEvent):
    """
        Поиск имени группы.
    """
    args = event.object.object.message.text.split()[1:]
    if len(args) == 0:
        return MSG_NO_NAME_GROUP

    groups = await find_groups_name(args[0])
    if groups == []:
        return MSG_GROUPS_IN_BD_NOT_FOUND

    mess = ""
    for x in groups:
        mess += x
        # чтобы не получить ошибку, введен лимит
        if (len(mess)) >= 500:
            mess = mess[0:mess.rfind('\n')]
            break
        mess += "\n"
    return MSG_GROUPS_IN_BD_FOUND + mess
