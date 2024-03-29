"""
    Файл с функциями взаимодействий с классом Group.
"""

from pskgu_bot.db.models import Group, Key
from pskgu_bot.db import local_storage
from pskgu_bot.utils import get_today, get_week_days, STRUCTED_DICT
from copy import deepcopy


async def find_all_groups():
    """
        Находит все имена групп и преподавателей.
    """
    return [x.name async for x in Group.find()]


async def check_group(name):
    """
        Проверяет находится ли группа в локальном
        хранилище по совпадению имени.
    """
    return (name in await local_storage.get(Key("groups")))


async def find_groups_name(name):
    """
        Находит имена групп в локальном
        хранилище по совпадению имени.
    """
    groups = []
    for x in await local_storage.get(Key("groups")):
        if x.find(name) != -1:
            groups.append(x)
    return groups


async def find_group_by_name(name):
    """
        Находит одну группу или преподавателя.
    """
    if name in await local_storage.get(Key("groups")):
        return await Group.find_one(filter={"name": name})
    return None


async def update_group(name, page_hash, prefix, days, page_url):
    """
        Обновление и создание документа группы или преподавателя.
    """
    def generate_upd_days(days_old, days_new):
        """
            Создаёт словарь с изменёнными днями на этой и следующей неделе.
        """
        # days = get_week_days(n=0) + get_week_days(n=1)
        days_upd = {'created': [], 'deleted': [], 'updated': {}}
        """
        Нужен рефакторинг кода!
        for day in days:
            value_old = days_old.get(day)
            value_new = days_new.get(day)
            if value_old == value_new:
                continue
            elif value_old is None and value_new:
                days_upd["created"].append(day)
            elif value_old and value_new is None:
                days_upd["deleted"].append(day)
            else:
                # TODO: добавить изменение значений.
                days_upd["updated"].update(
                    {day: {
                        "old": value_old,
                        "new": value_new
                    }})
        """
        return days_upd

    def generate_information(group):
        """
            Генерирует информацию об изменениях группы.
        """
        mess = "Произошло обновление - " + group.name + "\n"
        mess += "Дата: " + group.last_updated + "\n"
        mess += "Изменились:\n"
        if "page_url" in group.updated_items:
            mess += " - url страницы\n"
            mess += group.page_url + "\n"
        if "page_hash" in group.updated_items:
            mess += " - хеш страницы\n"
        if "days" in group.updated_items:
            mess += " - некоторые недели\n"
            upd_days = group.updated_days
            if upd_days == {'created': [], 'deleted': [], 'updated': {}}:
                return mess
            mess += "На текущей и(или) следующей неделе изменились дни:\n"
            if upd_days["created"] != []:
                mess += (" - созданы: " +
                         "".join(x + ", " for x in upd_days["created"]) + "\n")
            if upd_days["deleted"] != []:
                mess += (" - удалены: " +
                         "".join(x + ", " for x in upd_days["deleted"]) + "\n")
            if upd_days["updated"] != {}:
                mess += (" - изменены: " +
                         "".join(x + ", " for x in upd_days["updated"]) + "\n")
        return mess

    group = await Group.find_one(filter={"name": name})

    if not group:
        group = Group(
            name=name,
            days=days,
            page_hash=page_hash,
            prefix=prefix,
            page_url=page_url,
            last_updated=get_today(),
            updated_items=["days", "page_url", "prefix", "page_hash"])
    else:
        group.updated_items = []
        # при добавлении проверки на prefix в следующий if просиходит баг:
        # не видит изменения в других атрибутах, кроме prefix и
        # добавляет в l_s.updated_groups два раза имя группы
        # не понятна причина бага, следует проверить в будущем
        if group.page_hash != page_hash or group.page_url != page_url:
            if group.days != days:
                group.updated_days = generate_upd_days(group.days, days)
                group.days = days
                group.updated_items.append("days")
            if group.page_url != page_url:
                group.page_url = page_url
                group.updated_items.append("page_url")
            if group.prefix != prefix:
                group.prefix = prefix
                group.updated_items.append("prefix")
            if group.page_hash != page_hash:
                group.page_hash = page_hash
                group.updated_items.append("page_hash")
            group.last_updated = get_today()
            group.updated_information = generate_information(group)
    if group.updated_items != []:
        upd_groups = await local_storage.get(Key("updated_groups"))
        upd_groups.append(group.name)
        await local_storage.put(Key("updated_groups"), upd_groups)
    await group.commit()


async def create_structured_rasp():
    """
        Создаёт структурированое расписание.
    """
    def insert_empty_or_unfound_prep(s, name, key=None):
        """
            Вставка преподавателя без кафедры
            или не найденной кафедры в списке
        """
        if not key:
            s['преподаватель']['Прочее']['прочее'][
                "Кафедра отсутствует"].append(name)
            return

        if not s['преподаватель']['Прочее']['прочее'].get(key):
            s['преподаватель']['Прочее']['прочее'].update({key: []})
        s['преподаватель']['Прочее']['прочее'][key].append(name)
        return

    def insert_prep(s, name, key):
        flag = False
        for _, k2 in s['преподаватель'].items():
            for _, k3 in k2.items():
                for k4, v in k3.items():
                    if key == k4:
                        v.append(name)
                        flag = True
        if not flag:
            insert_empty_or_unfound_prep(structured, name, key)

    prefixes = set([tuple(x.prefix) async for x in Group.find()])
    prefixes = sorted(prefixes, key=lambda x: x[-1])
    structured = deepcopy(STRUCTED_DICT)

    for p in prefixes:
        if p[0] == "преподаватель":
            n = p[1].split(", ", 1)
            n[0] = n[0].replace(" ", "_")
            if not len(n) > 1:
                insert_empty_or_unfound_prep(structured, n[0])
            elif n[1] == 'кафедра':
                insert_empty_or_unfound_prep(structured, n[0])
            else:
                insert_prep(structured, n[0], n[1])
        else:
            if not structured[p[0]].get(p[1]):
                structured[p[0]].update({p[1]: {}})
                for i in range(1, 7, 1):
                    structured[p[0]][p[1]].update({str(i): []})
            if not structured[p[0]][p[1]].get(p[2]):
                structured[p[0]][p[1]].update({p[2]: []})
            structured[p[0]][p[1]][p[2]].append(p[3].replace(" ", "_"))

    # смена имен
    structured["Расписание студентов ОФО и ОЗФО"] = structured.pop("ОФО")
    structured["Расписание студентов ЗФО"] = structured.pop("ЗФО")
    structured["Расписание преподавателей"] = structured.pop("преподаватель")
    return structured
