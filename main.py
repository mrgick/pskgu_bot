#config
from config import *
#for vk bot
from vkwave.bots import SimpleLongPollBot
#keyboard
from vkwave.bots.utils.keyboards import Keyboard
#for storage
from vkwave.bots.storage.storages import Storage
from vkwave.bots.storage.types import Key
#for time
import datetime
#for db
import motor.motor_asyncio
#for initialize storage
import asyncio

#find in database key with name
async def db_find_one(name):
	mongo_url = await storage.get(Key("MONGO_URL"))
	client = motor.motor_asyncio.AsyncIOMotorClient(mongo_url)
	db = client['DB']
	collection = db['rasp']
	values = await collection.find_one({'name': name})
	return values 



#инициализация бота
bot = SimpleLongPollBot(tokens=token, group_id = group_id)

#начать
@bot.message_handler(bot.text_contains_filter("начать") | bot.text_contains_filter("start"))
async def handle(event: bot.SimpleBotEvent) -> str:
	kb = Keyboard(one_time=True,inline=False)
	kb.add_text_button("справка")
	kb.add_row()
	kb.add_link_button(text="расписание",link="http://rasp.pskgu.ru")
	await event.answer(message="выберите", keyboard=kb.get_keyboard())

# нужно понять каллбак с payload
@bot.message_handler(bot.text_contains_filter("faq") | bot.text_contains_filter("справка"))
async def handle(event: bot.SimpleBotEvent) -> str:
	
	mess="общий вид команды:\nпоказать  имя (группа или человек)  неделя (по умолчанию стоит текущая, +1 -> след., а -1 -> пред.)\n\nпример команды: \nпоказать 0431-06 +1\n(даная команда покажет следующую неделю группы 0431-06)"
	await event.answer(message=mess)

#вывод недели	
@bot.message_handler(bot.text_contains_filter("show") | bot.text_contains_filter("показать"))
async def handle(event: bot.SimpleBotEvent) -> str:
	
	mess="Данной записи в бд нет, либо команда неверно введена"
	args = event.object.object.message.text.split()[1:]

	#Проверяем есть ли аргументы
	if len(args)>0:
		#проверяем первый аргумент (имя)
		ALL=await storage.get(Key("ALL"))
		if ALL.get(args[0])!=None:
			data = await db_find_one(args[0])
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

	await event.answer(message=mess+"\n")




if __name__=="__main__":
	asyncio.get_event_loop().run_until_complete(initialize_storage())
	bot.run_forever()
