import os
from vkwave.bots import SimpleLongPollBot
import asyncio
#для хранилища
from utils.storage import storage, initialize_storage
from utils.parser import parser
from blueprints import (
	begin_router,
	help_router,
	week_router,
	subscription_router
)

#инициализация бота
bot = SimpleLongPollBot(tokens=os.environ.get('TOKEN_VK'), group_id = os.environ.get('GROUP_ID'))

#наши роутеры
bot.dispatcher.add_router(subscription_router)
bot.dispatcher.add_router(week_router)
bot.dispatcher.add_router(help_router)
bot.dispatcher.add_router(begin_router)



if __name__=="__main__":
	#создаем loop
	loop=asyncio.get_event_loop()
	#создаем хранилище
	loop.run_until_complete(initialize_storage())
	#запускаем бота
	loop.create_task(bot.run(ignore_errors=True))
	#запускаем парсер
	loop.create_task(parser())
	#заставляем работать вечно
	loop.run_forever()