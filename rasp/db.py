# Интерфейс для взаимодействия с базой данных.

import calendar
import asyncio

data_base_dict = []

# Инициализация базы данных.
def init():
    pass

# Проверка на существование в базе данных.
async def is_valid(name):
    return False

# Сверяет хеш страницы с базой данных.
async def check_hash(name, page_hash):
    return True

async def create(name, page_hash):
    pass

async def change(name, page_hash):
    pass

class Page:

    def push(self, name, page_hash):
        pass
        #data_base_dict[name] = { "page_hash": page_hash }


class Schedule:

    class Exporter:

        def make_week_range_iter():
            pass

        def make_week_iter():
            pass

        def make_day_iter():
            pass

        def make_class_iter():
            pass

        def __init__(self, export_iter=None, empty=False, start=None, end=None):
            self.export_iter = export_iter
            self.empty = empty
            self.start = start
            self.end = end

    class ClassExporter:
        def __init__(self, empty=False):
            pass

    class MergeDiff:
        pass
    
    # Форматирует сообщение для экспорта в текст.
    def export_text_format(msg, 
            cur_time=None, 
            this_time=None):
        if msg == "not_found":
            return "Расписание не обнаружено."
        if msg == "week_lost":
            return "\t%s\n\t*Расписание на данную неделю утеряно*\n\n"
        if msg == "week_empty":
            return "\t%s\n\t*На данной неделе нет ни одной пары*\n\n"
        if msg == "week_yet":
            return "\t%s\n\t*Расписания на данную неделю ещё нет*\n\n"
        if msg == "week":
            return "\t%s\n"

    def parse(self, parse_iter, today):
        self.weeks = []
        self.week_range = []
        cur_week = None
        tmtuple = today.timetuple()
        cur_mday = tmtuple.tm_mday
        cur_month = tmtuple.tm_mon
        week_idx = 0

        for week_table in parse_iter:
            week_table.idx = week_idx
            week_table.range_idx = 0
            week_table.days = []
            day_idx = 0

            for day in week_table.day_iter:
                day.idx = day_idx

                if cur_mday == day.day and cur_month == day.month:
                    cur_week = week_table

                day.classes = []
                for cur_class in day.class_iter:
                    day.classes.append(vars(cur_class))

                if len(day.classes) > 0:
                    day_dict = vars(day)
                    del day_dict["day"]
                    del day_dict["month"]
                    del day_dict["class_iter"]
                    week_table.days.append(day_dict)

                day_idx += 1

            if len(week_table.days) > 0:
                week_dict = vars(week_table)
                del week_dict["day_iter"]
                self.weeks.append(week_dict)
            week_idx += 1

        if not cur_week:
            self.week_range.append(None)
            return

        cur_week_time = calendar.timegm((tmtuple.tm_year, tmtuple.tm_mon, tmtuple.tm_mday - tmtuple.tm_wday, 0, 0, 0, 0, 0, 0))
        week_delta = 604800.0    
        cur_week_idx = cur_week.idx

        self.week_range.append([ cur_week_time - week_delta*cur_week_idx, cur_week_time + week_delta*(week_idx - cur_week_idx) ])


    async def push(self, name, page_hash):
        async with asyncio.Lock():

            name=name.replace(" ","_")
            name=name[0:20]

            days_name=["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"]
            weeks_new=[]
            for x in self.weeks:
              number_week=str(x.get("idx"))
              days=x.get("days")
              days_new=""
              for y in days:
                  number_day=y.get("idx")
                  days_new=days_new+days_name[number_day]+"\n"
                  days_text=y.get("classes")
                  for z in days_text:
                      dn=str(z.get("idx")+1)
                      dv=z.get("desc")
                      days_new=days_new+dn+")"+dv+"\n"
                  days_new=days_new+"\n"
              weeks_new.append({number_week:days_new})
              days_new=""

            data_base_dict.append({
                "name":name,
                "hash": page_hash,
                "text": weeks_new,
                "week_range": self.week_range
            })


    async def fetch(self, week_start, week_end):
        pass

    def merge(self, schedule):
        pass
    
    def export_ical(self):
        pass

    def export_text(self, 
            week_start, 
            week_end=None, 
            this_time=None, 
            day_idx=None, 
            title=None, 
            title_arg=None):

        header = export_text_format(title, title_arg=title_arg)
        if len(self.weeks) == 0:
            return export_text_format("not_found", header=header)

        week_idx = 0
        week_delta = 604800.0
        week_time = week_start
        week_iter = iter(self.weeks)
        cur_week = next(week_iter)
        week_range_idx = 0
        for cur_week_range in self.week_range:
            if cur_week_range and cur_week_range[0] >= week_start:
                if cur_week["range_idx"] == week_range_idx:
                    pass
                    
                elif cur_week["range_idx"] > week_range_idx:
                    pass
                

            week_range_idx += 1


class ScheduleList:
    def __init__(self):
        self.dict = {}

    def append(self, title):
        self.dict[title] = True

    async def push(self, name, page_hash):
        """
        async with asyncio.Lock():
            data_base_dict[name] = {
                "page_hash": page_hash,
                "dict": self.dict
            }
        """
        pass
    async def fetch(self):
        pass
    
    def merge(self, schedule_list):
        pass
