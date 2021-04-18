
import config
import logging
import asyncio
from data_types import DBKey
from db import mongodb

import clcontrol
from clients import vk

# Обёртка базы данных
db_wrapper = None


logger = logging.getLogger("pskgu-bot")

def init_db():
    """
    Инициализирует базу данных.
    Если база данных не указана, произойдёт ошибка.
    """

    if config.OPT_USE_MONGODB:
        use_mongodb()
    else:
        logger.error("База данных не указана!")
        exit(1)

    loop = asyncio.get_event_loop()
    status = loop.run_until_complete(db_wrapper.fetch("status"))
    if status.ex:
        logger.error("%s <Failed>: %s" % (db_wrapper, status.ex))
        exit(1)
    else:
        logger.info("%s <OK>: %s" % (db_wrapper, status.msg))


def sync():
    """
    Начинает синхронизацию базы данных с расписанием.
    """
    pass

def use_mongodb():
    """
    Инициализирует mongodb
    """
    global db_wrapper

    if not config.MONGODB_URL:
        logger.error(
            "MONGODB_URL is missing! Please, define this to use mongodb.")
        exit(1)

    if not config.MONGODB_NAME:
        logger.error(
            "MONGODB_NAME is missing! Please, define this to use mongodb.")
        exit(1)

    logger.info("Using mongodb...")
    db_wrapper = mongodb.MongoDB(url=config.MONGODB_URL,
                                name=config.MONGODB_NAME)
        

def start_all():
    """ 
    Запускает всех ботов (клиентов).
    """
    start_vk()

def append_client(cl):
    loop = asyncio.get_event_loop()
    status = loop.run_until_complete(clcontrol.append(cl))

    if status.ex:
        logger.error("%s <Failed>: %s" % (cl, status.ex))
    else:
        logger.info("%s <OK>: %s" % (cl, status.msg))

def start_vk():
    """
    Запускает VK бота.
    """
    if not config.VK_API_TOKEN:
        logger.error(
            "VK_API_TOKEN is missing! Please, define this to start VK bot.")
        return

    if not config.VK_GROUP_ID:
        logger.error(
            "VK_GROUP_ID is missing! Please, define this to start VK bot.")
        return
    logger.info("Starting VK bot...")

    append_client(
        vk.VKBot(api_token=config.VK_API_TOKEN, 
                    group_id=config.VK_GROUP_ID)
    )

    
        
def finish():
    """
    Завершает работу
    """
    logger.info("EXIT")

    tasks = []
    if db_wrapper:
        tasks.append(db_wrapper.close())

    clcontrol.close_all(tasks)
    
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))

