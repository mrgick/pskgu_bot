import asyncio
import hashlib
import aiohttp
from vkwave.bots.storage.types import Key

from config import bot, REMOTE_URL
from utils import web_db
from utils.storage import storage, initialize_storage
from utils.log import logger
import parser_module.parser

#test=True
#отправка сообщения определенному пользователю
async def send_message(message,user_id):
    await bot.api_context.messages.send(message=message,peer_id=user_id,random_id=0)

#Для теста сделан парсер, в дальнейшем переделать
async def parser():
    hash_db = await web_db.hash_main_page()

    #for test
    #url="https://pskgu.000webhostapp.com/"
    
    while True:
        try:
            hash_now = await get_page(REMOTE_URL)
            if hash_now != hash_db:
                hash_db = await web_db.hash_main_page(hash_now,insert=True)
                
                #парсер, запуск
                await parser_module.parser.run_parser()
                #обрабатываем ответ парсера
                try:
                    tasks = []
                    for value in parser_module.parser.data_base_dict:
                       tasks.append(asyncio.create_task(web_db.rasp_insert(value)))
                    await asyncio.wait(tasks)
                except Exception as e:
                    logger.error(e)

                logger.info(web_db.updated_list_rasp)
                parser_module.parser.data_base_dict = []
                #перезапускаем хранилище
                await initialize_storage()

                #!переписать рассылку + добавить обновления (изменился кабинет и т.д.)
                #рассылка уведомлений
                
                subs = await storage.get(Key("SUBS"))
                message="Произошло изменение расписания, либо обновилась ссылка."
                for x in subs:
                    if x.get("name") in web_db.updated_list_rasp:
                        for i in x.get("list"):
                            await send_message(message,i)
                

            await asyncio.sleep(60)
        
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(1800)
        
        finally:
            parser_module.parser.data_base_dict = []
            web_db.updated_list_rasp = []

#Асинхронно получает страницу и её хеш.
async def get_page(full_url="http://rasp.pskgu.ru/"):
    async with aiohttp.ClientSession() as session:
        async with session.get(full_url) as response:
            html = await response.read()
            return hashlib.sha1(html).hexdigest()


