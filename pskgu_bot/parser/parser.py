from .models import Route
from .parsing_page import parse_urls, parse_schedule
from pskgu_bot.db.services import update_group
from pskgu_bot.utils import logger
from pskgu_bot import Config
from asyncio import Semaphore, sleep, wait, create_task
import aiohttp
import hashlib
import re

semaphore = Semaphore(Config.SEMAPHORE)


async def start_parser():
    """
        Запускает парсер.
    """
    root = Route("")
    page = await get_page(root.url)
    if page:
        r = await get_anchors_and_run_async(route=root, page=page, regex=0)
    else:
        logger.critical("No urls on main page!")


async def get_page(url):
    """
        Асинхронно получает html страницу в виде байт-строки.
    """
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    await sleep(0.01)  # иногда нужна задержка
                    html = await response.read()
                    return html
            except Exception as e:
                logger.error("get url " + url + "|" + e)
                return None


def get_hash(page):
    """
        Получает хеш страницы.
    """
    return hashlib.sha1(page).hexdigest()


async def get_anchors_and_run_async(route, page, regex):
    """
        Запускает асинхронно в generate_by_regex
        каждый отдельный экземпляр класса Anchor.
    """
    try:
        tasks = []
        for anchor in parse_urls(page, route, regex):
            tasks.append(
                create_task(
                    generate_by_regex(parent=route, anchor=anchor,
                                      regex=regex)))
        if tasks != []:
            await wait(tasks)
    except Exception as e:
        logger.error(e)


async def generate_by_regex(parent, anchor, regex=0):
    """
        Обрабатывает ссылки, генерирует маршруты.
        p.s. для ОФО и ЗФО нужно два раза пройтись
        по ссылкам, а для преподавателей - один раз.
    """
    def valid(item, title, regex):
        """
            Проверяет на валидность имени.
            Нужен для нахождения определенных ссылок на главной странице.
        """
        if regex == 0:
            if not re.match(item, title):
                return False
        return True

    if regex == 0:
        list_regex = [
            [r"(.*очно-заочной*)", "ОФО", 2],
            [r"(.*заочной формы*)", "ЗФО", 2],
            [r"(.*Преподаватели*)", "преподаватель", 1]
        ]

    else:
        list_regex = [[None, anchor.title, 1]]

    for item in list_regex:
        if valid(item[0], anchor.title, regex):
            route = Route(anchor.href, parent, item[1], anchor.course)
            if route.valid:
                page = await get_page(route.url)
                if page:
                    if regex == 1:
                        await generate_group(route=route,
                                             page=page,
                                             title=anchor.title)
                    else:
                        await get_anchors_and_run_async(route=route,
                                                        page=page,
                                                        regex=item[2])


async def generate_group(route, page, title):
    """
        Генерирует расписание в готовом виде.
    """
    def normolize_name(name, prefix):
        """
            Преобразует имя в нормальный вид.
        """
        if name.find(" ") == -1:
            return name
        elif prefix != "преподаватель":
            return name.replace(" ", "_")
        else:
            return name.split(",")[0].replace(" ", "_")

    try:
        page_hash = get_hash(page)
        prefix = route.prefix
        days = parse_schedule(page)
        name = normolize_name(title, prefix[0])
        url = route.url
        await update_group(name, page_hash, prefix, days, url)
        logger.info(name + " " + prefix[0])
    except Exception as e:
        logger.error(title + " " + route.url + " " + str(e))
