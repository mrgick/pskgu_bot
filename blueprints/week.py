from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	CommandsFilter,
)
#for storage
from vkwave.bots.storage.types import Key
#заставляем увидеть mongo_db и storage
import sys
sys.path.append('../')
from utils.storage import storage
from mongo_db.db import db_find_name
#for translations
import googletrans
#for time
import datetime


week_router = DefaultRouter()


#вывод недели   
@simple_bot_message_handler(week_router, CommandsFilter(commands=("show", "показать"), prefixes=("/")))
async def handle(event: SimpleBotEvent) -> str:
	
	mess="Данной записи в бд нет, либо команда неверно введена"
	args = event.object.object.message.text.split()[1:]

	#Проверяем есть ли аргументы
	if len(args)>0:
		#проверяем первый аргумент (имя)
		all_names = await storage.get(Key("ALL"))
		if (args[0] in all_names)==True:
			data = await db_find_name(args[0])
			data=data.get('text')
			
			#проверяем второй аргумент (число)
			n=0
			if len(args)>1:
				try:
					n=int(args[1])
				except:
					pass

			#поиск текущей недели в словаре (костыль, нужно будет переделать)
			week=int(datetime.datetime.utcnow().strftime('%V'))+n #номер недели
			for number, text in data.items():
				if week == int(datetime.datetime.fromtimestamp(int(number)).strftime('%V')):
					mess=text
			mess="Имя: "+args[0]+"; Неделя: "+str(week)+"\n"+mess
			
			#проверка 3 аргумента
			if len(args)>2:
				#перевод
				if googletrans.LANGUAGES.get(args[2])!=None:
					try:
						mess = googletrans.Translator().translate('Перевод может содержать ошибки.\n'+mess,src="ru",dest=args[2]).text
					except Exception as e:
						#print(e)
						mess = 'Sorry, translation failed. Please try again later.'

			

			"""         
						#заменить time.mktime на calendar.timegm в парсере
						week=week_now(n)
						if data.get(week)!=None:
							mess=data.get(week)
	mess+"\n"+str(week_tests())
			"""                 
	await event.answer(message=mess)


#поиск имени
@simple_bot_message_handler(week_router, CommandsFilter(commands=("find", "поиск"), prefixes=("/")))
async def handle(event: SimpleBotEvent) -> str:
	args = event.object.object.message.text.split()[1:]
	#Проверяем есть ли аргументы
	if len(args)>0:
		all_names = await storage.get(Key("ALL"))
		message="похожие записи в базе данных:\n"
		#ищем подстроку в строке в массиве
		for x in all_names:
			if x.find(args[0])!=-1:
				message=message+x+"\n"
			#чтобы не получить ошибку(макс лимит сообщения), делаем не больше 500
			if (len(message))>=500:
				message=message[0:message.rfind('\n')]
				break
	else:
		message="вы не указали аргумент(имя)"       
	await event.answer(message=message)
