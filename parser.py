
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
import lxml.html
import os.path
import re

MAX_REQUEST_AMOUNT = 10

debug_logger = logging.getLogger(config.DEBUG_LOGGER)

class Page():
    pass

request_semaphore = asyncio.Semaphore(MAX_REQUEST_AMOUNT)

def get_hash(text):
    return hashlib.sha1(text).hexdigest()

async def request(url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                return await response.read()
    except aiohttp.web.HTTPClientError as ex:
        raise errors.RequestError(url, ex)

def get_html_tree(html):
    html = (html.replace(
        b"--!>", b"-->").replace(
        b"<tbody>", b"").replace(
        b"</tbody>", b""))

    if html.find(b"charset=") == -1:
        html_parser = lxml.html.HTMLParser(encoding="windows-1251")
        return lxml.html.fromstring(html, parser=html_parser)
    else:
        return lxml.html.fromstring(html)


def normalize_suffix(url_suffix):
    return url_suffix.replace("\\", "/")


async def get_page(url_suffix):
    full_url = config.SCHEDULE_URL + url_suffix
    async with request_semaphore:
        debug_logger.debug("Requesting '%s'..." % full_url)
        html = await request(full_url)
        result_page = Page()
        result_page.html = html
        result_page.full_url = full_url
        result_page.url_suffix = url_suffix
        result_page.hash = get_hash(html)
        result_page.html_tree = get_html_tree(html)
        return result_page

def check_regex_list(text, regex_list):
    for (regex, entry_class, title) in regex_list:
        m = re.search(regex, text)
        if m:
            return (entry_class, title or m.group(0))
    return (None, None)

def suffix_join(base_suff, suff):
    if not suff:
        return base_suff

    (head, trail) = os.path.split(base_suff)
    return os.path.join(head, normalize_suffix(suff))

class BaseEntry():
    def __init__(self, base_suffix, url_suffix, title=None):
        self.title = title
        self.url_suffix = suffix_join(base_suffix, url_suffix)

    def anchors(self, xpath):
        for x in self.page.html_tree.xpath(xpath):
            yield (
                x.get("href"),
                x.text_content(),
            )

    def links(self):
        static = type(self)
        xpath = static.link_xpath
        regex_list = static.link_regex

        for (href, text) in self.anchors(xpath):
            if href == "#":
                continue

            (entry_class, title) = check_regex_list(text, 
                                                    regex_list)
            if entry_class:
                yield entry_class(
                            base_suffix=self.page.url_suffix, 
                                url_suffix=href, title=title)

    async def enter(self):
        entry_page = await get_page(self.url_suffix)
        self.page = entry_page
        

class ScheduleEntry(BaseEntry):

    month_dict = {
        "янв": 1,
        "фев": 2,
        "мар": 3,
        "апр": 4,
        "мая": 5,
        "июн": 6,
        "июл": 7,
        "авг": 8,
        "сен": 9,
        "окт": 10,
        "ноя": 11,
        "дек": 12,
    }

    def parse(self):
        schedule = data_types.FetchSchedule(
                url_suffix = self.url_suffix,
                page_hash=self.page.hash,
                title=self.title)
                

        week_tables = self.page.html_tree.xpath(".//table")
        self.parse_weeks(schedule, week_tables)
        return schedule
        
    def parse_weeks(self, schedule, week_tables):
        for week_table in week_tables:
            week = data_types.FetchWeek(parent=schedule)
            day_rows = iter(week_table.xpath("tr"))
            # Пропустить заголовок
            next(day_rows)
            next(day_rows)
            #
            self.parse_days(schedule, week, day_rows)
            if week:  
                if (schedule.has_new_year and
                        not week.is_new_year_boundary):
                    schedule.has_new_year = False
                    week.is_new_year = True
                schedule.append(week)
            elif week.is_new_year:
                schedule.has_new_year = True


    def parse_days(self, schedule, week, day_rows):
        day_idx = 0
        for day_row in day_rows:
            class_cols = iter(day_row.xpath("td"))
            date = next(class_cols).text_content().strip()

            m = re.search("\S+\s*,(\d+)\s*(\S{3})", date)
            month_day = int(m.group(1), 10)
            month = ScheduleEntry.month_dict[m.group(2)]
            
            day = data_types.FetchDay(
                        parent=week,
                        idx=day_idx, 
                        month=month, 
                        month_day=month_day)


            prev_day = schedule.prev_day
            if prev_day:
                if prev_day.month == 12 and day.month != 12:
                    schedule.has_new_year = True
                    week.prev_year_day = prev_day
                    week.is_new_year_boundary = True

            if day_idx == 0: # Понедельник
                if schedule.has_new_year:
                    schedule.has_new_year = False
                    week.is_new_year = True

                week.month = month
                week.month_day = month_day

            self.parse_classes(day, class_cols)
            if day:
                week.append(day)

            day_idx += 1
            schedule.prev_day = day

    def parse_classes(self, day, class_cols):
        class_idx = 0
        for class_col in class_cols:
            desc = class_col.text_content().strip()
            if desc and desc != "_":
                day.append(
                    data_types.FetchClass(
                        parent=day,
                        idx=class_idx, desc=desc))
            class_idx += 1

class GroupScheduleEntry(ScheduleEntry):
    pass

class TeacherScheduleEntry(ScheduleEntry):
    pass

class GroupEntry(BaseEntry):
    link_xpath = ".//table/tr/td/p/a"
    link_regex = [
        ( r"(.*)", GroupScheduleEntry, None )
    ]

class TeacherEntry(BaseEntry):
    link_xpath = ".//table/tr/td/p/a"
    link_regex = [
        ( r"(.*)", TeacherScheduleEntry, None )
    ]

class InstEntry(BaseEntry):
    link_xpath = ".//a"
    link_regex = [
        ( r"(.*)", GroupEntry, None )
    ]

class FullTimeEntry(InstEntry):
    link_xpath = InstEntry.link_xpath
    link_regex = InstEntry.link_regex

class ExtEntry(InstEntry):
    link_xpath = InstEntry.link_xpath
    link_regex = InstEntry.link_regex

class RootEntry(BaseEntry):
    link_xpath = ".//a"
    link_regex = [
        ( r"(.*ОФО.*)", FullTimeEntry, "ОФО" ),
        ( r"(.*ЗФО.*)", ExtEntry, "ЗФО" ),
        ( r"(.*преподав.*)", TeacherEntry, "Преподаватели" )
    ]

    def __init__(self):
        super().__init__(base_suffix="", 
                        url_suffix="", title="Расписание")



            

async def enter_root():
    root = RootEntry()

    await root.enter()

    return root

def print_schedule(prefix, schedule):
    for week in schedule:
        week.make_datetime()
        print(prefix, week.datetime.strftime(
                    "%Yг, Неделя в году: %W"))
        for day in week:
            day.make_datetime()
            print(prefix, "\t", day.datetime.strftime("%A, %d %B"))
            for day_class in day:
                day_class.make_datetime()
                print(prefix, "\t\t",
                    "Пара №%i" % (day_class.idx + 1),
                        day_class.datetime.strftime("%H:%M"), "-", 
                        day_class.end_datetime.strftime("%H:%M"),
                        ":")
                print(prefix, "\t\t\t", day_class.desc)
            print(prefix, "\t", "==============================") 

def print_merged(prefix, schedule):

    prefix_list = [ "=", "+", "-", "*" ]

    for week in schedule:
        
        print(prefix, 
            prefix_list[week.merge_method], 
                    week.datetime.strftime(
                    "%Yг, Неделя в году: %W"))
        for day in week:
            day_prefix = prefix_list[day.merge_method]
            print(prefix, day_prefix,
                "\t", day.datetime.strftime("%A, %d %B"))

            for day_class in day:
                class_method = day_class.merge_method
                class_prefix = prefix_list[class_method]
                
                print(prefix, class_prefix, "\t\t",
                    "Пара №%i" % (day_class.idx + 1),
                        day_class.datetime.strftime("%H:%M"), "-", 
                        day_class.end_datetime.strftime("%H:%M"),
                        ":")
                if class_method == data_types.MERGE_METHOD.CHANGED:
                    print(prefix, class_prefix + "+", 
                        "\t\t\t", "СТАЛО:", day_class.desc)

                    print(prefix, class_prefix + "-", 
                        "\t\t\t", "БЫЛО:", day_class.old_desc)
                else:
                    print(prefix, class_prefix, 
                        "\t\t\t", day_class.desc)



            print(prefix, day_prefix, 
                "\t", "==============================") 

async def test_parse():

    import datetime

    now = datetime.datetime.now()
    root = await enter_root()
    for category in root.links():
        #print(category.title)
        if isinstance(category, InstEntry):
            await category.enter()
            for inst in category.links():
                await inst.enter()
                if isinstance(inst, GroupEntry):
                    #print("\t", inst.title)
                    for group in inst.links():
                        if isinstance(group, GroupScheduleEntry):
                            await group.enter()
                            schedule = group.parse()
                            schedule.sync_time(now)

                            #print("\t\t", "Группа", group.title)
                            print_schedule("\t\t\t|", schedule)
                            return schedule

        elif isinstance(category, TeacherEntry):
            await category.enter()
            for teacher in category.links():
                if isinstance(teacher, TeacherScheduleEntry):

                    await teacher.enter()
                    schedule = teacher.parse()

                    schedule.sync_time(now)

                    #print("\t", "Преподаватель", teacher.title)
                    print_schedule("\t\t|", schedule)

def test_modify(schedule):
    schedule.weeks[0].days[0].classes[0].desc = "123"

async def test_do_work():

    import locale

    locale.setlocale(locale.LC_TIME, "ru_RU.UTF-8")



    schedule = await test_parse()
    copied = schedule.copy()
    print_schedule("ORIG|", schedule)
    print("==============================")
    test_modify(copied)
    print_schedule("COPY|", copied)
    print("==============================")


    print_merged("MERGED|",
        copied.merge(schedule, data_types.MERGE_METHOD.KEEP))


    
if __name__ == "__main__":
    config.SCHEDULE_URL = "http://rasp.pskgu.ru/"
    event_loop = asyncio.get_event_loop()
    EVEnt_loop.run_until_complete(test_do_work())


