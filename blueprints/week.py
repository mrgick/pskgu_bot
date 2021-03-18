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
import calendar


week_router = DefaultRouter()


#вывод недели   
@simple_bot_message_handler(week_router, CommandsFilter(commands=("show", "показать"), prefixes=("/")))
async def handle(event: SimpleBotEvent) -> str:
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

			#поиск текущей недели в словаре (костыль, нужно будет переделать)
			message="Нет данных\n"
			week=int(datetime.datetime.utcnow().strftime('%V'))+n #номер недели
			number=data.get('week_range')[0][0]
			print(number)
			tmtuple=datetime.datetime.utcnow().timetuple()
			cur_week_time = 604800*n+calendar.timegm((tmtuple.tm_year, tmtuple.tm_mon, tmtuple.tm_mday - tmtuple.tm_wday, 0, 0, 0, 0, 0, 0))

			i=0
			while i<len(data.get('text')):
				if cur_week_time >= number and cur_week_time <= (number+604800):
					message = data.get('text')[i+1].get(str(i+1))
					break
				else:
					number=number+604800
					i=i+1

			message="Имя: "+args[0]+"; Неделя: "+str(week)+"\n"+message
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
