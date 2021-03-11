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
	if len(args)>0:
		all_names = await storage.get(Key("ALL"))
		#проверяем правильно ли введено имя
		if args[0] in all_names:
			user_id=event.object.object.message.peer_id
			subs= await storage.get(Key('SUBS'))
			#надо будет переделать, но пока так
			k=0#для ветвления
			n=-1
			i=0
			while i<len(subs):
				if args[0]==subs[i].get('name'):
					n=i
				if user_id in subs[i].get('list'):
					message = "вы уже подписаны на "+subs[i].get('name')
					k=1
				i=i+1
			if k==0:
				result = await do_insert_user_id(args[0],user_id)
				if subs !=[] and n!=-1:
					subs[n]=result
					print(subs)
				else:
					subs.append(result)
				await storage.put(Key('SUBS'),subs)
				message="теперь вы подписаны"
				

		else:
			message="данное имя не найдено в бд, проверьте правильность ввода"
	else:
		message="введите имя(группу или преподавателя), на которую хотите подписаться"
	await event.answer(message=message)

#отписаться
@simple_bot_message_handler(subscription_router, CommandsFilter(commands=("отписаться", "unsubscribe"), prefixes=("/")))
async def subcribe(event: SimpleBotEvent) -> str:
	user_id=event.object.object.message.peer_id
	subs= await storage.get(Key('SUBS'))
	k=0
	i=0
	while i<len(subs):
		if user_id in subs[i].get('list'):
			result = await del_user_id(subs[i].get('name'),user_id)
			message = "теперь вы отписаны от "+subs[i].get('name')
			subs[i]=result
			print(subs)
			await storage.put(Key('SUBS'),subs)
			i=len(subs)
			k=1
		i=i+1

	if k==0:
		message="вы не подписаны на уведомления"
	await event.answer(message=message)