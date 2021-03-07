#config
from config import *
#for vk bot
from vkwave.bots.utils.keyboards import Keyboard
from vkwave.bots.utils.keyboards.keyboard import ButtonColor
from vkwave.bots import SimpleLongPollBot
from vkwave.bots import CallbackAnswer, PayloadFilter, TextFilter
from vkwave.types.bot_events import BotEventType
#for db
import pymongo
#for time
import datetime

#find in database key with name
def db_read(name):
	try:
		client = pymongo.MongoClient(mongo_url)
		db = client['DB']
		collection = db['rasp']
		return collection.find_one({'name':name})
	except pymongo.errors:
		print(e)
	finally:
		client.close()

#инициализация бота
bot = SimpleLongPollBot(tokens=token, group_id=group_id)

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
		if ALL.get(args[0])!=None:
			data=db_read(args[0]).get('text')
			
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
	bot.run_forever()

