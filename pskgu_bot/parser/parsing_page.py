"""
    Предназначен для парсинга расписания на странице
"""

from .models import Anchor
from pskgu_bot import Config
from pskgu_bot.utils import date_to_str, logger
import re
import lxml.html
import datetime

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


def lxml_parce(html):
    """
        Получение lxml парсинга страницы.
        Нужен, так как html страницы местами содержат баги:
        (не указана кодировка, неправильный комментарий и т.д.)
    """
    def normolize_html(html):
        html = html.replace(b"--!>", b"-->")
        html = html.replace(b"<tbody>", b"")
        html = html.replace(b"</tbody>", b"")
        return html

    def have_enconding(html):
        return html.find(b"charset=") != -1

    html = normolize_html(html)

    if not have_enconding(html):
        myparser = lxml.html.HTMLParser(encoding='windows-1251')
        return lxml.html.fromstring(html, parser=myparser)
    else:
        return lxml.html.fromstring(html)


def parse_urls(html):
    """
        Парсит ссылки со страницы, в дальнейшем называемые якорями.
    """
    html = lxml_parce(html)
    return ((Anchor(x.xpath("@href")[0], x.text_content())
             for x in html.xpath(".//a")))


def parse_schedule(html):
    """
        Парсит расписание c html страницы
    """
    def normolize_text(text):
        """
            Чистит текст от лишних символов.
        """
        text = text.replace("\r\n", "")
        text = text.replace("\n", " ")
        text = text.replace("_", " ")
        text = text.replace("  ", " ")
        return text

    def good_text(text):
        """
            Проверяет текст, на наличие букв или цифр.
        """
        return re.search(r"[а-яА-ЯёЁ]|[a-z-A-Z]|[0-9]", text) is not None

    def get_date(text):
        """
            Возвращает отформатированое время.
        """
        text = text.split(",")[1]
        text = text.replace(" ", "")
        try:
            date = datetime.datetime.strptime(text, '%d.%m.%Y')
            text = date_to_str(date)
            return text
        except Exception as e:
            logger.error(e)
            return None

    html = lxml_parce(html)
    data = {}

    for table in html.xpath("/html/body/table"):
        for item, tr in enumerate(table.xpath("tr")):
            if item < 2:
                continue
            day = {}
            day_date = ""
            for i, td in enumerate(tr.xpath('td')):

                # fix spaces
                for br in td.xpath("*//br"):
                    br.tail = " " + br.tail if br.tail else " "

                text = normolize_text(td.text_content())
                if i == 0:
                    day_date = get_date(text)
                    continue
                if good_text(text):
                    day.update({str(i): text})
            if day != {} and day_date:
                data.update({day_date: day})

    return data
