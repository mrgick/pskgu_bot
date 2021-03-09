#config
from config import *
#for vk bot
from vkwave.bots import SimpleLongPollBot
#keyboard
from vkwave.bots.utils.keyboards import Keyboard
#for storage
from vkwave.bots.storage.storages import Storage
from vkwave.bots.storage.types import Key
#for initialize storage
import asyncio
#for time
import datetime

#import time
#import pytz

#for db
import motor.motor_asyncio


"""
TODO: 
-нужно понять callback и payload
-сделать поиск по именам
-сделать перевод на англ, при помощи google translate 
-!пофиксить поиск в бд на сервере (частично понял, для начала нужно переделать парсер)
-!сделать пост уведомления об изменении
"""

#инициалицазия mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
#инициализация бота
bot = SimpleLongPollBot(tokens=token, group_id = group_id)

"""
def week_now(n=0):
	time_now=datetime.datetime.now(pytz.timezone('Europe/London'))
	monday = time_now - datetime.timedelta(days = time_now.weekday()-7*n)
	moday_zero = datetime.datetime(monday.year, monday.month, monday.day)
	number=str(int(time.mktime(moday_zero.timetuple())))
	return number

def week_tests(n=0):
	time_now=datetime.datetime.now(pytz.timezone('Europe/London'))
	monday = time_now - datetime.timedelta(days = time_now.weekday()-7*n)
	moday_zero = datetime.datetime(monday.year, monday.month, monday.day)
	number=str(int(time.mktime(moday_zero.timetuple())))
	return time_now,monday,moday_zero,number
"""
#поиск определенного значения по ключу name
async def do_find_all_names(db="DB",collection="rasp"):
	db = client[db]
	collection = db[collection]
	all_names=[]
	async for document in collection.find({}):
		all_names.append(document['name'])
	return all_names


#Хранилице данных, которые берутся несколько раз
storage = Storage()
async def initialize_storage():
	all_dict = Key("ALL")
	ALL= await do_find_all_names()
	await storage.put(all_dict, ALL)

#поиск определенного значения по ключу name
async def db_find_name(name, db="DB",collection="rasp"):
	db = client[db]
	collection = db[collection]
	values = await collection.find_one({'name': name})
	return values 

#начать
@bot.message_handler(bot.text_contains_filter("начать"))
async def handle(event: bot.SimpleBotEvent) -> str:
	kb = Keyboard(one_time=True,inline=False)
	kb.add_text_button("/help")
	kb.add_row()
	kb.add_link_button(text="расписание",link="http://rasp.pskgu.ru")
	await event.answer(message="Выберите действие", keyboard=kb.get_keyboard())

#справка
@bot.message_handler(bot.command_filter(commands=("help", "справка"), prefixes=("/")))
async def handle(event: bot.SimpleBotEvent) -> str:
	
	mess="общий вид команды:\n/показать(или /show)  имя (группа или человек)  неделя (по умолчанию стоит текущая, +1 -> след., а -1 -> пред.)\n\nпример команды: \n/показать 0431-06 +1\n(даная команда покажет следующую неделю группы 0431-06)"
	await event.answer(message=mess)

#вывод недели	
@bot.message_handler(bot.command_filter(commands=("show", "показать"), prefixes=("/")))
async def handle(event: bot.SimpleBotEvent) -> str:
	
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
			week=int(datetime.datetime.utcnow().strftime('%V'))+n-1 #номер недели
			for number, text in data.items():
				if week == int(datetime.datetime.fromtimestamp(int(number)).strftime('%V')):
					mess=text
			mess="Имя: "+args[0]+"; Неделя: "+str(week)+"\n"+mess
			
			"""			
						#заменить time.mktime на calendar.timegm в парсере
						week=week_now(n)
						if data.get(week)!=None:
							mess=data.get(week)
	mess+"\n"+str(week_tests())
			"""					
	await event.answer(message=mess)


#поиск имени
@bot.message_handler(bot.command_filter(commands=("find", "поиск"), prefixes=("/")))
async def handle(event: bot.SimpleBotEvent) -> str:
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



if __name__=="__main__":
	asyncio.get_event_loop().run_until_complete(initialize_storage())
	bot.run_forever()

