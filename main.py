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

#Хранилице данных, которые берутся несколько раз
storage = Storage()
async def initialize_storage():
	all_dict = Key("ALL")
	ALL={'0431-01': 'Inst6_0431_01', '0022-01': 'Inst6_0022_01', '0023-01': 'Inst6_0023_01', '0024-01': 'Inst6_0024_01', '0431-02': 'Inst6_0431_02', '0022-02': 'Inst6_0022_02', '0023-02': 'Inst6_0023_02', '0024-02': 'Inst6_0024_02', '0431-03': 'Inst6_0431_03', '0022-03': 'Inst6_0022_03', '0023-03': 'Inst6_0023_03', '0024-03': 'Inst6_0024_03', '0431-04': 'Inst6_0431_04', '0022-04': 'Inst6_0022_04', '0023-04': 'Inst6_0023_04', '0024-04': 'Inst6_0024_04', '0431-05': 'Inst6_0431_05', '0022-05': 'Inst6_0022_05', '0023-05': 'Inst6_0023_05', '0024-05': 'Inst6_0024_05', '0431-06': 'Inst6_0431_06', '0022-06': 'Inst6_0022_06', '0023-06': 'Inst6_0023_06', '0024-06': 'Inst6_0024_06', '0431-07': 'Inst6_0431_07', '0032-01': 'Inst6_0032_01', '0033-01': 'Inst6_0033_01', '0034-01': 'Inst6_0034_01', '0431-08': 'Inst6_0431_08', '0032-03': 'Inst6_0032_03', '0033-02': 'Inst6_0033_02', '0034-03': 'Inst6_0034_03', '0431-09': 'Inst6_0431_09', '0032-04': 'Inst6_0032_04', '0033-04': 'Inst6_0033_04', '0034-04': 'Inst6_0034_04', '0431-11': 'Inst6_0431_11', '0032-05': 'Inst6_0032_05', '0033-05': 'Inst6_0033_05', '0034-05': 'Inst6_0034_05', '0431-13': 'Inst6_0431_13', '0032-06': 'Inst6_0032_06', '0033-08': 'Inst6_0033_08', '0034-06': 'Inst6_0034_06', '0431-03М': 'Inst6_0431_03М', '0032-08': 'Inst6_0032_08', '0034-08': 'Inst6_0034_08', '0431-08М': 'Inst6_0431_08М', '0032-09': 'Inst6_0032_09', '0034-09': 'Inst6_0034_09', '0431-09М': 'Inst6_0431_09М', '0022-09М': 'Inst6_0022_09М', '0431-11М': 'Inst6_0431_11М', '0032-07М': 'Inst6_0032_07М', '2431-03М': 'Inst6_2431_03М', '2032-01М': 'Inst6_2032_01М', '2431-09М': 'Inst6_2431_09М'}
	await storage.put(all_dict, ALL)

#поиск определенного значения по ключу name
async def db_find_name(name):
	db = client['DB']
	collection = db['rasp']
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
		ALL=await storage.get(Key("ALL"))
		if ALL.get(args[0])!=None:
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




if __name__=="__main__":
	asyncio.get_event_loop().run_until_complete(initialize_storage())
	bot.run_forever()

