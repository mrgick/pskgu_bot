from vkwave.bots.storage.types import Key
#заставляем увидеть mongo_db и storage

import sys
sys.path.append('../')
from utils.storage import storage,initialize_storage

async def test():
	#проверка ALL
	all_names = await storage.get(Key("ALL"))
	print("1):",all_names)
	await storage.put(Key("ALL"),[])
	all_names = await storage.get(Key("ALL"))
	print("2)",all_names)


if __name__=="__main__":
	import asyncio
	loop = asyncio.get_event_loop()
	loop.run_until_complete(initialize_storage())
	loop.run_until_complete(test())
