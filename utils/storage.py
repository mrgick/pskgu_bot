from vkwave.bots.storage.storages import Storage
from vkwave.bots.storage.types import Key
#заставляем увидеть mongo_db
import sys
sys.path.append('../')

from mongo_db.db import do_find_all_names, do_find_all_subs

#Хранилице данных, которые берутся несколько раз
storage=Storage()
async def initialize_storage():
	#список всех групп, преподавателей
	all_names= await do_find_all_names()
	await storage.put(Key("ALL"), all_names)
	#список подписчиков, людей, которым должно придти уведомление
	subscribers = await do_find_all_subs()
	await storage.put(Key("SUBS"), subscribers)


"""
#для тестов
if __name__=="__main__":
	import asyncio
	loop = asyncio.get_event_loop()
	loop.run_until_complete(initialize_storage())
"""