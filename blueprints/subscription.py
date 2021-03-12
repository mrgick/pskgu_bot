from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	CommandsFilter,
)
#for storage
from vkwave.bots.storage.types import Key
from utils.storage import storage
from utils.web_db import do_insert_user_id, del_user_id

subscription_router = DefaultRouter()

#подписаться
@simple_bot_message_handler(subscription_router, CommandsFilter(commands=("подписаться", "subscribe"), prefixes=("/")))
async def subcribe(event: SimpleBotEvent) -> str:
	args = event.object.object.message.text.split()[1:]
	#проверяем первый аргумент
	if len(args) > 0:
		all_names = await storage.get(Key("ALL"))
		#проверяем правильно ли введено имя
		if args[0] in all_names:
			user_id = event.object.object.message.peer_id
			subs = await storage.get(Key('SUBS'))
			do_insert=True
			index_number=-1
			for x in subs:
				if args[0] == x.get('name'):
					index_number=subs.index(x)
				if user_id in x.get('list'):
					message = "Вы уже подписаны на "+x.get('name')+"."
					do_insert=False
			#делаем вставку
			if do_insert:
				result = await do_insert_user_id(args[0],user_id)
				if subs!=[] and index_number!=-1:
					subs[index_number]=result
				else:
					subs.append(result)
				await storage.put(Key('SUBS'),subs)
				#print(subs)
				message="Теперь вы подписаны на "+args[0]+"."
		else:
			message="Данное имя:"+args[0]+" не найдено в бд, проверьте правильность ввода."
	else:
		message="Введите имя(группу или преподавателя), на которую хотите подписаться."
	await event.answer(message=message)

#отписаться
@simple_bot_message_handler(subscription_router, CommandsFilter(commands=("отписаться", "unsubscribe"), prefixes=("/")))
async def subcribe(event: SimpleBotEvent) -> str:
	user_id=event.object.object.message.peer_id
	subs = await storage.get(Key('SUBS'))
	user_not_in_list=True
	for x in subs:
		if user_id in x.get('list'):
			result = await del_user_id(x.get('name'),user_id)
			subs[subs.index(x)]=result
			await storage.put(Key('SUBS'),subs)
			message = "Теперь вы отписаны от "+x.get('name')+"."
			user_not_in_list=False
			#print(subs)
			break		
	if user_not_in_list:
		message="Вы не подписаны на уведомления."
	await event.answer(message=message)