# Предназначен для парсинга расписания на странице
import re
import lxml.html
import datetime

#класс Якорь, пошло от html тега <a>
class Anchor:
    def __init__(self, href, title):
        self.href = href
        self.title = title

def lxml_parce(html):
    html = html.replace(b"--!>", b"-->")
    html = html.replace(b"<tbody>",b"")
    html = html.replace(b"</tbody>",b"")
    if html.find(b"charset=") == -1:
        myparser = lxml.html.HTMLParser(encoding='windows-1251')
        return lxml.html.fromstring(html,parser=myparser)
    else:
        return lxml.html.fromstring(html)
            

# Парсит ссылки со страницы; в дальнейшем называются якорями
def parse_urls(html):
    html = lxml_parce(html)
    return ((Anchor(str(x.xpath("@href")[0]), str(x.text_content())) for x in html.xpath(".//a")))
    

#нужно произвести refactoring нижних функций

# Парсит расписание.
def parse_schedule(html):
    html = lxml_parce(html)
    i = 0
    data = {}

    for table in html.xpath("/html/body/table"):
        c = []
        #print(table.text_content())
        for tr in table.xpath("tr"):
            #print(tr.text_content())
            d = []
            for td in tr.xpath('td'):
                text = td.text_content().replace("\r\n","").replace("\n"," ").replace("_"," ")
                d.append(text)
            c.append(d)
        data.update({i:c})
        i = i + 1
    return arr_print(data)


#перобразуем массив во второй раз
def arr_print(arr):
    def no_good_text(text):
        #проверка текста, на содержание букв или цифр
        if re.search(r"[а-яА-ЯёЁ]|[a-z-A-Z]|[0-9]", text) == None:
            return True
        else:
            return False


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

    data={}
    for k in range(len(arr)):
        #print(arr[k][2][0])

        # Получаем время понедельника, каждой таблицы в секундах
        try:
            m = re.match(r".*\s*\,(\d+)\s*(.{3})", arr[k][2][0])
            day, month = int(m.group(1), 10), MONTH_NAMES[m.group(2).lower()]
            t = datetime.datetime(2021, month, day)
            name_time = str(datetime.datetime.timestamp(t))
            if "." in name_time:
              name_time = name_time.split(".")[0]
        except:
            continue

        # Получаем дни
        days={}
        for i in range(len(arr[k])):
            if no_good_text(arr[k][i][0]):
                continue
            if i >= 2:
                day = i-1

                # Получаем пары
                lessons = {}
                for x in range(len(arr[k][i])):
                    if no_good_text(arr[k][i][x]):
                        continue
                    else:
                        if x>=1:
                            lessons.update({str(x):arr[k][i][x]})
                
                if lessons != {}:
                    days.update({str(day):lessons})
            if days != {}:
                data.update({str(name_time):days})
    
    return data
