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


def parse_urls(html, route, regex):
    """
        Парсит ссылки со страницы, в дальнейшем называемые якорями.
    """
    html = lxml_parce(html)
    # такая схема нужна, чтобы спарсить курс
    if regex == 1:
        if route.prefix[0] != "преподаватель":
            anchors = []
            table = html.xpath(".//table")[0]
            for tr in table.xpath("tr"):
                for item, td in enumerate(tr.xpath("td"), 1):
                    a = td.xpath("a")
                    if len(a) > 0:
                        anchors.append(
                            Anchor(a[0].xpath("@href")[0], a[0].text_content(),
                                   item))
            return anchors
    return ((Anchor(x.xpath("@href")[0], x.text_content())
             for x in html.xpath(".//a")))


def parse_schedule(html):
    """
        Парсит расписание c html страницы
    """
    def normolize_text(text, version):
        """
            Чистит текст от лишних символов.
        """
        if version == "prev":
            text = text.replace("\r\n", "")
            text = text.replace("\n", " ")
            text = text.replace("_", " ")
        elif version == "post":
            while '  ' in text:
                text = text.replace('  ', ' ')
            text = text.strip()
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

    for table in html.xpath(".//table"):
        for item, tr in enumerate(table.xpath("tr")):
            if item < 2:
                continue
            day = {}
            day_date = ""
            for i, td in enumerate(tr.xpath('td')):
                divs = []
                text = ""

                # парсинг в виде списоков
                if i != 0:
                    for div in td.xpath("div"):
                        div1 = []
                        if div.text:
                            div1.append(normolize_text(div.text, 'post'))
                        for br in div.xpath("br"):
                            if br.tail:
                                div1.append(normolize_text(br.tail, 'post'))
                        if div1 != []:
                            divs.append(div1)

                # парсинг в виде строки
                if i == 0 or divs == []:
                    for elem in td.xpath(".//*"):
                        elem.tail = " " + elem.tail if elem.tail else " "
                    text = normolize_text(td.text_content(), "prev")

                    if i == 0:
                        day_date = get_date(text)
                        continue

                if good_text(text) or divs != []:

                    if divs == []:
                        text = normolize_text(text, "post")
                        divs.append(text)

                    day.update({str(i): divs})

            if day != {} and day_date:
                data.update({day_date: day})

    return data
