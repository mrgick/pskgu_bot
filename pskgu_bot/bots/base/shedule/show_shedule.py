from pskgu_bot.bots.base.messages import (MSG_NO_NAME_GROUP,
                                          msg_not_found_group_name)

from pskgu_bot.db.services import (find_vk_user_by_id, find_group_by_name)
from pskgu_bot.utils import get_week_days, get_name_of_day, str_to_int
from typing import Optional


async def show_schedule(user_id: Optional[str] = None,
                        group_name: Optional[str] = None,
                        week_shift: Optional[str] = None,
                        type_sys: str = "vk") -> str:
    """
        Возвращает расписание недели.
    """
    def make_readable_text(group, keys):
        """
            Преобразуем словарь group.days в читаемое сообщение.
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

    if (group_name is None or group_name == ""):
        group_name = None

    user_id = str_to_int(user_id)

    week_shift = str_to_int(week_shift)
    if week_shift is None:
        week_shift = 0

    if (user_id is not None and group_name is None and type_sys == "vk"):
        user = await find_vk_user_by_id(user_id)
        if user:
            group_name = user.group

    if (group_name is None or group_name == ""):
        return MSG_NO_NAME_GROUP

    group = await find_group_by_name(group_name)
    if not group:
        return msg_not_found_group_name(group_name)

    mess = ""
    days = get_week_days(week_shift)
    mess += add_name(mess, group)
    mess += "Ссылка: " + group.page_url + "\n"
    mess += make_readable_text(group, days)

    return mess
