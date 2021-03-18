import asyncio
import hashlib
import aiohttp
from config import bot
from utils.web_db import hash_main_page, rasp_insert
#хранилище внутреннее
from utils.storage import storage, initialize_storage
from vkwave.bots.storage.types import Key

import rasp.generate_route
import rasp.db

rasp.generate_route.semaphore = asyncio.Semaphore(10)
test=True
#отправка сообщения определенному пользователю
async def send_message(message,user_id):
	await bot.api_context.messages.send(message=message,peer_id=user_id,random_id=0)

#Для теста сделан парсер, в дальнейшем переделать
async def parser():
	url = "http://rasp.pskgu.ru/"
	hash_db = await hash_main_page()

	#for test
	#url="https://pskgu.000webhostapp.com/"
	
	while True:
		try:
			hash_now = await get_page(url)
			if hash_now != hash_db:
				hash_db = await hash_main_page(hash_now,insert=True)
				
				#парсер, запуск
				rasp.db.data_base_dict=[]
				await rasp.generate_route.generate_route()

				#обрабатываем ответ парсера
				updated_list = await rasp_insert(rasp.db.data_base_dict)
				
				#перезапускаем хранилище
				await initialize_storage()

				#рассылка уведомлений
				subs = await storage.get(Key("SUBS"))
				message="Произошло изменение расписания."
				for x in subs:
					if x.get("name") in updated_list:
						for i in x.get("list"):
							await send_message(message,i)

			await asyncio.sleep(300)
		except Exception as e:
			print(e)

#Асинхронно получает страницу и её хеш.
async def get_page(full_url="http://rasp.pskgu.ru/"):
	async with aiohttp.ClientSession() as session:
		async with session.get(full_url) as response:
			html = await response.read()
			return hashlib.sha1(html).hexdigest()
