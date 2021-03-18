# Автоматически генерирует маршрут.
# Вначале лучше почитать комментарии в rasp/route.py

import rasp.route
import rasp.parser
import rasp.config
import rasp.db

import hashlib
import os.path
import asyncio
import aiohttp
from datetime import datetime
import hashlib
import lxml.html
import re

# Корень маршрута.
root = None


# Добавить в список задач.
def ensure_future(tasks, asyncfunc):
    tasks.append(asyncio.ensure_future(asyncfunc))

# Асинхронно получает страницу и её хеш.
async def get_page(route):
    full_url = os.path.join(rasp.config.REMOTE_URL, route.url)
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            async with session.get(full_url) as response:
                html = await response.read()
                html = html.replace(b"--!>", b"-->")
                #print(full_url)
                if html.find(b"charset=")==-1:
                    myparser=lxml.html.HTMLParser(encoding='windows-1251')
                    return (lxml.html.fromstring(html,parser=myparser), hashlib.sha1(html).hexdigest())
                else:
                    return (lxml.html.fromstring(html), hashlib.sha1(html).hexdigest())

# Генерирует маршрут по списку регулярных выражений.
# Регулярные выражения состоят из:
#   Само регулярное выражение;
#   Хеш-строка (Да, можно было бы использовать заголовок,
#               но заголовки могут изменяться);
#   Заголовок;
#   Коллбэк.
async def generate_by_regex(regex, parent, anchor, teacher=None):
    title = anchor.title
    for item in regex:
        # Находит совпадения с регулярными выражениями.
        m = re.match(item[0], title)
        if m:
            # Создаёт узел маршрута с URL, как у якоря.
            route = rasp.route.Route(parent, item[1], anchor.href, item[2])
            route.teacher = teacher
            # Проверяет узел на действительность.
            if route.valid:
                page, page_hash = await get_page(route)
                # Вызывает коллбэк (Передаёт текущий маршрут, страницу,
                # хеш страницы и захваченный регулярным выражением заголовок).
                await item[3](route, page, page_hash, m.group(1))

# Записать расписание в базу данных.
async def make_schedule_db(html_element, name, page_hash):
    if await rasp.db.is_valid(name):
        pass
    else:
        schedule = rasp.db.Schedule()
        schedule.parse(rasp.parser.parse_schedule(html_element), datetime.now())
        await schedule.push(name, page_hash)

# Записать список с расписаниями в базу данных.
async def make_list_db(route, html_element, name, page_hash, regex, is_teacher_list=False):
    schedule_list = rasp.db.ScheduleList()
    tasks = []
    for anchor in rasp.parser.parse_anchors(html_element):
        title = anchor.title
        teacher = None
        # Если это список преподавателей, получить хеш от названия преподавателя.
        if is_teacher_list:
            teacher = str(title.encode("windows-1251"))
            title = teacher
            

        schedule_list.append(title)
        ensure_future(tasks, generate_by_regex(regex, route, anchor, teacher=teacher))
    await schedule_list.push(name, page_hash)
    await asyncio.wait(tasks)

# Генерирует расписание для студентов.
async def generate_inst_schedule(route, page, page_hash, title):
    route.title = title
    await route.join(title)
    await make_schedule_db(page.find("body"), title, page_hash)

# Регулярные выражения для расписания студентов.
ROUTE_INST_SCHEDULE_REGEX = [
    ["(.*)", None, None, generate_inst_schedule]
]

# Генерирует институты.
async def generate_inst(route, page, page_hash, title):
    route.title = title
    name = os.path.basename(route.url_dir)
    await route.join(name)
    await make_list_db(route, page.find("body").find("table"), name, page_hash, ROUTE_INST_SCHEDULE_REGEX)

# Регулярные выражения для институтов.
ROUTE_INST_REGEX = [
    [r"(.*)", None, None, generate_inst]
]

async def generate_students(route, html_element, page_hash, title, regex):
    tasks = []
    for anchor in rasp.parser.parse_anchors(html_element):
        ensure_future(tasks, generate_by_regex(regex, route, anchor))
    await asyncio.wait(tasks)

# Генерирует ОФО.
async def generate_ext_fulltime(route, page, page_hash, title):
    await route.join("ft")
    await generate_students(route, page.find("body") or page, page_hash, title, ROUTE_INST_REGEX)

# Генерирует расписание преподавателя.
async def generate_teacher_schedule(route, page, page_hash, title):
    route.title = title

    # Вставить в словарь хеш от названия преподавателя.
    #name = route.teacher
    await route.join(title) 

    await make_schedule_db_teach(page.find("body"), title, page_hash)



# Записать расписание в базу данных.
async def make_schedule_db_teach(html_element, name, page_hash):
    if await rasp.db.is_valid(name):
        pass
    else:
        schedule = rasp.db.Schedule()
        schedule.parse(rasp.parser.parse_schedule_tch(html_element), datetime.now())
        await schedule.push(name, page_hash)


# Регулярные выражения для списка преподавателей.
ROUTE_TEACHERS_REGEX = [
    [r"(.*)", None, None, generate_teacher_schedule]
]

# Генерирует список преподавателей.
async def generate_teachers(route, page, page_hash, title):
    await route.join("tch")
    await make_list_db(route, page.find("body").find("table"), "tch", page_hash, ROUTE_TEACHERS_REGEX, is_teacher_list=True)


# Регулярные выражения для корня.
ROUTE_ROOT_REGEX = [
    [r"(.*ОФО.*)", "ft", "Очная форма обучения (ОФО)", generate_ext_fulltime],
    [r"(.*ЗФО.*)", "ext", "Заочная форма обучения (ЗФО)", generate_ext_fulltime],
    #[r"(.*преподавателей.*)", "tch", "Преподаватели", generate_teachers],
]

# Генерирует корень.
async def generate_root(root):
    page, page_hash = await get_page(root)
    tasks = []
    for anchor in rasp.parser.parse_anchors(page.find("body")):
        ensure_future(tasks, generate_by_regex(ROUTE_ROOT_REGEX, root, anchor))
    await asyncio.wait(tasks)

# Генерирует весь маршрут.
async def generate_route():
    global root 
    root = rasp.route.Route(None, None, "") 
    # Проверяет корень на действительность.
    if root.valid:
        await generate_root(root)
    else:
        root = None
        raise GenerateRouteException("Couldn't generate the root!")


# Получить текущий корень.
def get_root():
    return root

