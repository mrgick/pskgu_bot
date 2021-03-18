# Предназначен для парсинга расписания,
# а также для поиска пути.

#import rasp.config

import urllib.request
import lxml.html
import lxml
import os.path
import re

class Anchor:
    def __init__(self, href, title):
        self.href = href
        self.title = title

class ScheduleWeekTable:
    def __init__(self, day_iter):
        self.day_iter = day_iter

class ScheduleDay:
    def __init__(self, class_iter, month, day):
        self.class_iter = class_iter
        self.month = month
        self.day = day

class ScheduleClass:
    def __init__(self, idx, desc):
        self.idx = idx
        self.desc = desc

# Парсит элемент.
def parse_element(html_element, tag):
    for x in html_element:
        if x.tag == tag:
            yield x
        else:
            yield from parse_element(x, tag)

# Парсит якори.
def parse_anchors(html_element):
    return (Anchor(x.get("href"), "".join(x.itertext())) for x in html_element.iterfind(".//a"))

def parse_desc(column):
    text = "".join(column.find(".//p").itertext())
    if not text or text == "_":
        return None
    return text

def parse_day(class_iter):
    i = 0
    while i < 7:
        desc = parse_desc(next(class_iter))
        if desc:
            yield ScheduleClass(i, desc) 
        i += 1

MONTH_NAMES = {
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
def parse_daymonth(column):
    text = "".join(column.find(".//p").itertext())
    m = re.match(r".*\s*\,(\d+)\s*(.{3})", text)
    return int(m.group(1), 10), MONTH_NAMES[m.group(2).lower()]

def parse_week_table(html_element):
    day_iter = html_element.iterfind("tr")
    
    # Пропустить заголовок.
    next(day_iter)
    next(day_iter)
    #
    for x in day_iter:
        class_iter = x.iterfind(".//td")
        day, month = parse_daymonth(next(class_iter))
        yield ScheduleDay(class_iter=parse_day(class_iter), 
                day=day, month=month)

# Парсит расписание.
def parse_schedule(html_element):
    for x in parse_element(html_element, "table"):
        yield ScheduleWeekTable(day_iter=parse_week_table(x))

# Парсит расписание перпод.
def parse_schedule_tch(html_element):
    #day_iter = html_element.iterfind("tr")
    #print(day_iter)
    for x in parse_element(html_element, "table"):    
        yield ScheduleWeekTable(day_iter=parse_week_table(html_element))