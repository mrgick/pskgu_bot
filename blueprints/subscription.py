from vkwave.bots import (
	DefaultRouter,
	simple_bot_message_handler,
	SimpleBotEvent,
	CommandsFilter,
)
#for storage
from vkwave.bots.storage.types import Key
from utils.storage import storage
from mongo_db.db import do_insert_user_id, del_user_id

subscription_router = DefaultRouter()

#реализовать рассылку!
#async def send_message(message,user_id):
#	await  bot.api_context.messages.send(message=message,random_id=0,user_id=user_id)


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
			n=-1
			for x in subs:
				if args[0] == x.get('name'):
					n=subs.index(x)
				if user_id in x.get('list'):
					message = "Вы уже подписаны на "+x.get('name')+"."
					do_insert=False
			#делаем вставку
			if do_insert:
				result = await do_insert_user_id(args[0],user_id)
				if subs!=[] and n!=-1:
					subs[n]=result
				else:
					subs.append(result)
				await storage.put(Key('SUBS'),subs)
				message="Теперь вы подписаны."
				#print(subs)
		else:
			message="Данное имя не найдено в бд, проверьте правильность ввода."
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