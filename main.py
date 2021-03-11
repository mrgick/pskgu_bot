import os
from vkwave.bots import SimpleLongPollBot

#для хранилища
import asyncio
from utils.storage import storage, initialize_storage

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
	asyncio.get_event_loop().run_until_complete(initialize_storage())
	bot.run_forever()