"""
    Файл вспомогательных функций
"""

from pskgu_bot import Config
from datetime import datetime, timedelta

DAYS_NAME = {
    0: "Понедельник",
    1: "Вторник",
    2: "Среда",
    3: "Четверг",
    4: "Пятница",
    5: "Суббота",
    6: "Воскресенье"
}


def date_to_str(date, full=False):
    """
        Перевод даты в строку с удалением  временной зоны.
    """
    if full:
        return str(date)
    return str(date).split(" ")[0]


def get_today(n=0, full=False):
    """
        Возвращает сегодняшний день со смещением.
    """
    time_now = datetime.now()
    time_now = time_now + timedelta(days=n)
    return date_to_str(time_now, full)


def get_str_date(day, month, year=Config.YEAR):
    """
        Возвращает дату в виде строки.
    """
    return date_to_str(datetime(year, month, day))


def get_week_days(n=0):
    """
        Возвращает список дней этой недели
        начиная с понедельника по субботу.
        n - смещение на количество недель.
    """
    days = []
    ntime = datetime.now()
    ntime = ntime + timedelta(days=-ntime.weekday(), weeks=n)
    for x in range(6):
        days.append(date_to_str(ntime))
        ntime = ntime + timedelta(days=1)
    return days


def get_name_of_day(str_date):
    """
        Возвращает имя дня.
    """
    day = datetime.fromisoformat(str_date).weekday()
    return DAYS_NAME.get(day)


def compare_str_date(date1, date2):
    """
        Сравнивает две даты в виде строк.
        date1 >= date2
    """
    return datetime.fromisoformat(date1) >= datetime.fromisoformat(date2)


def get_monday(date):
    """
        Возвращает понедельник недели c date.
    """
    date = datetime.fromisoformat(date)
    monday = date + timedelta(days=-date.weekday(), weeks=0)
    return date_to_str(date=monday)
