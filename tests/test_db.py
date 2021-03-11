import asyncio
import os
from mongo_db.db import *

#для проверки
async def test():
	a=await do_find_all_subs()
	print(a)


if __name__=="__main__":
	loop = asyncio.get_event_loop()
	loop.run_until_complete(test())
