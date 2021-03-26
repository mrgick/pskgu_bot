from parser_module import routes, parsing_page
from utils.log import logger
import asyncio
import aiohttp
import os
import hashlib
import re

data_base_dict = []

# Настройки парсера
REMOTE_URL = "http://rasp.pskgu.ru"
semaphore = asyncio.Semaphore(10)


# Запускает парсер
async def run(): 
    data_base_dict = []
    root = routes.Route(None, "")
    full_url = os.path.join(REMOTE_URL, root.url)
    page, _ = await get_page(full_url)
    if page != None:
        await run_all_anchors(route=root, page=page, regex=0, prefix="")
    else:
        logger.critical("no urls on main page")


# Такая конструкция очень много где повторялась, и я вынес её; p.s. нужно сменить имя.
async def run_all_anchors(route, page, regex, prefix):
    tasks = []
    for anchor in parsing_page.parse_urls(page):
       tasks.append(asyncio.create_task(generate_by_regex(parent=route, anchor=anchor, regex=regex, prefix=prefix)))
    await asyncio.wait(tasks)


# Асинхронно получает страницу и её хеш.
async def get_page(url):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    html = await response.text()
                    #для хеширования, нужна явная кодировка
                    if html.find("charset=") == -1:
                        page_hash = hashlib.sha1(html.encode("windows-1251")).hexdigest()
                    else:
                        page_hash = hashlib.sha1(html.encode("utf-8")).hexdigest()
                    #!нужно сделать задержку, иначе сайт расписания умирает
                    html = html.replace("--!>", "-->")
                    html=html.replace("<tbody>","")
                    html=html.replace("</tbody>","")
                    #logger.debug("get url " + url)
                    return (html, page_hash)

            except Exception as e:
                logger.error("in get url " + url)
                logger.error(str(e))
                return (None, None)


# Обрабатывает ссылки, генерирует маршруты
async def generate_by_regex(parent, anchor, regex=0, prefix=""):

    if regex == 0:
        regex = [
            [r"(.*ОФО.*)", "ОФО", generate_st_and_tch],
            [r"(.*ЗФО.*)", "ЗФО", generate_st_and_tch],
            [r"(.*препод.*)", "преподователь", generate_st_and_tch]
        ]
    elif regex == 1:
        regex = [
            ["(.*)", prefix, generate_inst]
        ]
    elif regex == 2:
        regex = [
            ["(.*)", prefix, generate_page_readble]
        ]

    for item in regex:
        m = re.match(item[0], anchor.title)
        if m:
            # Создаёт узел маршрута с URL, как у якоря.
            route = routes.Route(parent, anchor.href)
            # Проверяет узел на действительность.
            if route.valid:
                full_url = os.path.join(REMOTE_URL, route.url)
                page, page_hash = await get_page(full_url)
                await item[2](route, page, page_hash, anchor.title, item[1])


# Перебирает первые ссылки.
async def generate_st_and_tch(route, page, page_hash, title, prefix):
    if prefix == "ОФО" or prefix == "ЗФО":
        regex=1
    else:
        regex=2
    await run_all_anchors(route=route, page=page, regex=regex, prefix=prefix)


# Генерирует институты.
async def generate_inst(route, page, page_hash, title, prefix):
    await run_all_anchors(route=route, page=page, regex=2, prefix=prefix)


# Генерирует расписание в готовом виде.
async def generate_page_readble(route, page, page_hash, title, prefix):
    logger.debug(prefix+" "+title+" "+page_hash)
    try:
        weeks=parsing_page.parse_schedule(page)
        result={
            "name":title.replace(" ","_")[0:20],
            "page_hash":page_hash,
            "weeks":weeks,
        }

        data_base_dict.append(result)
    except Exception as e:
        logger.error(e)