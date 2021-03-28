from vkwave.bots import (
    DefaultRouter,
    simple_bot_message_handler,
    SimpleBotEvent,
    CommandsFilter,
)
#for storage
from vkwave.bots.storage.types import Key
from utils.storage import storage
from utils.web_db import db_find_name
#for translations
import googletrans
#for time
import datetime
import pytz

week_router = DefaultRouter()


#вывод недели   
@simple_bot_message_handler(week_router, CommandsFilter(commands=("show", "показать"), prefixes=("/")))
async def handle(event: SimpleBotEvent) -> str:

    # Получаем время недели
    def week_time(n=0):
        time_now = datetime.datetime.now(pytz.timezone("Europe/Dublin"))
        time_now = time_now + datetime.timedelta(days=-time_now.weekday(), weeks=n)
        year = int(time_now.strftime('%Y'))
        month = int(time_now.strftime('%m'))
        day = int(time_now.strftime('%d'))
        wanted_time = datetime.datetime(year, month, day)
        return str(datetime.datetime.timestamp(wanted_time)).split(".")[0]
    
    # Преобразуем словарь недели в читаемый вид
    def readable_text(arr,time):
        text = arr["weeks"].get(time)
        if text != None:
            week = ""
            days_name={"1":"Понедельник", "2":"Вторник", "3":"Среда", "4":"Четверг", "5":"Пятница", "6":"Суббота", "7":"Воскресенье"}
            for day, value in text.items():
                day_name = days_name.get(day)
                day = 86400 * (int(day) - 1) + int(time)
                day = datetime.datetime.fromtimestamp(day).strftime('%Y.%m.%d')
                week = week + str(day_name) + ", " + day + "\n"
                for x, lesson  in value.items():
                    week = week + x + ")" + lesson + "\n"
                week = week + "\n"
            return week
        else:
            return "Данная неделя не найдена."


    #получаем аргументы 
    args = event.object.object.message.text.split()[1:]
    #Проверяем есть ли аргументы
    if len(args) > 0:
        all_names = await storage.get(Key("ALL"))
        #проверяем первый аргумент (имя)
        if (args[0] in all_names)==True:
            data = await db_find_name(args[0])
            n = 0
            #проверяем второй аргумент (число)
            if len(args) > 1:
                try:
                    n=int(args[1])
                except:
                    pass

            
            #получаем текст недели
            t=week_time(n)
            time_now = datetime.datetime.now(pytz.timezone("Europe/Dublin"))
            message=readable_text(data,t) + str(time_now)



            message="Имя: "+args[0]+""+"\n\n"+message
            #проверка 3 аргумента
            if len(args) > 2:
                #проверяем есть ли такой префикс языка
                if googletrans.LANGUAGES.get(args[2]) != None:
                    try:
                        message = googletrans.Translator().translate('Перевод может содержать ошибки.\n'+message,src="ru",dest=args[2]).text
                    except:
                        message='Извините перевод завершился ошибкой. Попробуйте позднее.\n'+message
                else:
                    message='Данный префикс языка не обнаружен в базе данных.\n'+message
        else:
            message="Данное имя не обнаружено в базе данных. Для поиска имен воспользуйтесь командой /find"
    else:
        message="Вы не ввели аргумент(имя). Для просмотра справки введите /help"
    """         
    #заменить time.mktime на calendar.timegm в парсере
    week=week_now(n)
    if data.get(week)!=None:
        message=data.get(week)
        message+"\n"+str(week_tests())
    """                 
    await event.answer(message=message)


#поиск имени
@simple_bot_message_handler(week_router, CommandsFilter(commands=("find", "поиск"), prefixes=("/")))
async def handle(event: SimpleBotEvent) -> str:
    #получаем аргументы 
    args = event.object.object.message.text.split()[1:]
    #Проверяем есть ли первый аргумент
    if len(args) > 0:
        all_names = await storage.get(Key("ALL"))
        message=""
        #ищем подстроку в строке в массиве строк (тавтлогия)
        for x in all_names:
            if x.find(args[0]) != -1:
                message=message+x+"\n"
            #чтобы не получить ошибку(макс лимит сообщения), делаем не больше 500
            if (len(message)) >= 500:
                message=message[0:message.rfind('\n')]
                break
        if message != "":
            message="Похожие записи в базе данных:\n"+message
        else:
            message="Похожих записей в базе данных не найдено."
    else:
        message="Вы не ввели аргумент(имя). Пример команды: /find 01"
    await event.answer(message=message)
