from parser_module import routes, parsing_page
from utils.log import logger
from config import REMOTE_URL
import asyncio
import aiohttp
import os
import hashlib
import re

data_base_dict = []
semaphore = asyncio.Semaphore(20)


# Запускает парсер
async def run_parser(): 
    data_base_dict = []
    root=routes.Route(None,"", "")
    page = await get_page(REMOTE_URL)
    if page != None:
        await run_all_anchors(route=root, page=page, regex=0)
    else:
        logger.critical("no urls on main page")


# Такая конструкция очень много где повторялась, и я вынес её; p.s. нужно сменить имя.
async def run_all_anchors(route, page, regex):
    try:
        tasks = []
        for anchor in parsing_page.parse_urls(page):
           tasks.append(asyncio.create_task(generate_by_regex(parent=route, anchor=anchor, regex=regex)))
        await asyncio.wait(tasks)
    except Exception as e:
        logger.error(e)


# Асинхронно получает страницу и её хеш.
async def get_page(url):
    async with semaphore:
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url) as response:
                    #нужна задержка, иначе сайт расписания умирает
                    await asyncio.sleep(0.01)
                    
                    html = await response.text()
                    html = html.replace("--!>", "-->")
                    html=html.replace("<tbody>","")
                    html=html.replace("</tbody>","")
                    #logger.debug("get url " + url)
                    return html

            except Exception as e:
                logger.error("in get url " + url)
                logger.error(e)
                return None


# Обрабатывает ссылки, генерирует маршруты
async def generate_by_regex(parent, anchor, regex=0):

    if regex == 0:
        regex = [
            [r"(.*ОФО.*)", "ОФО", generate_st_and_tch],
            [r"(.*ЗФО.*)", "ЗФО", generate_st_and_tch],
            [r"(.*препод.*)", "преподователь", generate_st_and_tch]
        ]
    elif regex == 1:
        regex = [
            ["(.*)", parent.prefix, generate_inst]
        ]
    elif regex == 2:
        regex = [
            ["(.*)", parent.prefix, generate_page_readble]
        ]

    for item in regex:
        m = re.match(item[0], anchor.title)
        if m:
            # Создаёт узел маршрута с URL, как у якоря.
            route = routes.Route(parent, anchor.href, item[1])
            # Проверяет узел на действительность.
            if route.valid:
                full_url = os.path.join(REMOTE_URL, route.url)
                page = await get_page(full_url)
                await item[2](route, page, anchor.title)


# Перебирает первые ссылки.
async def generate_st_and_tch(route, page, title):
    if route.prefix == "ОФО" or route.prefix == "ЗФО":
        regex=1
    else:
        regex=2
    await run_all_anchors(route=route, page=page, regex=regex)


# Генерирует институты.
async def generate_inst(route, page, title):
    await run_all_anchors(route=route, page=page, regex=2)


# Генерирует расписание в готовом виде.
async def generate_page_readble(route, page, title):
    
    try:
        #для хеширования, нужна явная кодировка
        if page.find("charset=") == -1:
            page_hash = hashlib.sha1(page.encode("windows-1251")).hexdigest()
        else:
            page_hash = hashlib.sha1(page.encode("utf-8")).hexdigest()
        
        prefix = [route.prefix, route.url_dir]


        weeks=parsing_page.parse_schedule(page)
        result={
            "name":title.replace(" ","_")[0:20],
            "page_hash":page_hash,
            "prefix":prefix,
            "weeks":weeks
        }

        data_base_dict.append(result)
        logger.info(prefix[0]+" "+prefix[1]+" "+title+" "+page_hash)
    except Exception as e:
        logger.error(e)