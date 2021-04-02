import asyncio
from utils.storage import initialize_storage
from utils.parser import parser
from blueprints import (
	begin_and_help_router,
	week_router,
	map_router,
	subscription_router
)
from config import bot

"""
TODO:
-переделать /help
-переделать парсер (рефакторинг)
-переделать бд и вставку нового
-добавить ical
-сделать тесты
"""

#наши роутеры(события)
bot.dispatcher.add_router(subscription_router)
bot.dispatcher.add_router(week_router)
bot.dispatcher.add_router(map_router)
bot.dispatcher.add_router(begin_and_help_router)


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