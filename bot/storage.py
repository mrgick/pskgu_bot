from vkwave.bots.storage.storages import Storage
from vkwave.bots.storage.types import Key
from db import do_find_all_names
#Хранилице данных, которые берутся несколько раз
storage=Storage()
async def initialize_storage():
	all_dict = Key("ALL")
	ALL= await do_find_all_names()
	await storage.put(all_dict, ALL)