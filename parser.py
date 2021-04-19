
import logging
import hashlib
import asyncio
import aiohttp
import aiohttp.web
import config
import data_types
import errors
import mods
import components

MAX_REQUEST_AMOUNT = 10

debug_logger = logging.getLogger(config.DEBUG_LOGGER)

class Page():

    def parse_tags(self, element):
        pass

    def parse_anchors(self, element):
        pass

    def parse_week_tables(self, element):
        pass


request_semaphore = asyncio.Semaphore(MAX_REQUEST_AMOUNT)

def get_hash(html):
    return hashlib.sha1(html).hexdigest()

async def request(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return response
    except aiohttp.web.HTTPClientError as ex:
        raise errors.RequestError(url, ex)

async def get_page(url_suffix):
    full_url = config.SCHEDULE_URL + "/" + url_suffix
    async with request_semaphore:
        debug_logger.debug("Requesting '%s'..." % full_url)
        response = await request(full_url)
        html = await response.read()
        result_page = Page()
        result_page.html = html
        result_page.full_url = full_url
        result_page.url_suffix = url_suffix
        result_page.hash = get_hash(html)
        return result_page

class BaseEntry():
    def __init__(self, url_suffix, name, title=None):
        self.name = name
        self.title = title
        self.url_suffix = url_suffix

    def links(self):
        
        

    async def enter(self):
        entry_page = await get_page(self.url_suffix)
        self.page = entry_page

        

class RootEntry(BaseEntry):
    link_regex = [
        ( r"(.*ОФО.*)", FullTimeEntry, "ОФО" ),
        ( r"(.*ЗФО.*)", ExtEntry, "ЗФО" ),
        ( r"(.*преподав.*)", TeacherEntry, "Преподаватели" )
    ]

    def __init__(self):
        super.__init__(url_suffix="", name="root", title="Расписание")

class InstEntry(BaseEntry):
    link_regex = [
        ( r"(.*)", GroupEntry, None )
    ]

class FullTimeEntry(InstEntry):
    link_regex = InstEntry.link_regex

class ExtEntry(InstEntry):
    link_regex = InstEntry.link_regex

class TeacherEntry(BaseEntry)
    link_regex = [
        ( r"(.*)", TeacherScheduleEntry, None )
    ]


class Parser(components.BaseComponent):

    async def status(self):
        url = config.SCHEDULE_URL
        try:
            await request(url)
        except errors.RequestError as ex:
            raise errors.StatusError(ex)

        raise errors.StatusSuccess(
            "'%s' is avaliable." % url)

    async def parse_groups(self):
        pass

    async def parse_teachers(self):
        pass


 
