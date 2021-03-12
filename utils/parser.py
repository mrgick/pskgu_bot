import asyncio
import hashlib
import aiohttp
from config import bot
from utils.web_db import hash_main_page

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
				#здесь должен запускаться парсер страниц
				messages="Произошло изменение расписания."
				await send_message(messages,74091241)
			await asyncio.sleep(300)
		except:
			pass

#Асинхронно получает страницу и её хеш.
async def get_page(full_url="http://rasp.pskgu.ru/"):
	async with aiohttp.ClientSession() as session:
		async with session.get(full_url) as response:
			if response.status != 200:
				raise GenerateRouteException("Failed to connect to %s!" % full_url, status=response.status)
			html = await response.read()
			return hashlib.sha1(html).hexdigest()
