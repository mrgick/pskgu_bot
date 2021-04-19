
import config
import errors
import logging
import asyncio
import parser
from data_types import DBKey
from db import mongodb

import sync_strategy
import clcontrol
from clients import vk

# Обёртка базы данных
db_wrapper = None


logger = logging.getLogger(config.PSKGU_BOT_LOGGER)
event_loop = asyncio.get_event_loop() 

def get_db():
    return db_wrapper

async def check_status(component):
    try:
        await component.status()
    except errors.StatusSuccess as ex:
        return (True, ex)
    except errors.StatusError as ex:
        return (False, ex)

def init():
    mods.init_db()
    mods.init_clients()
    mods.init_sync()

def init_db():
    """
    Инициализирует базу данных.
    Если база данных не указана, произойдёт ошибка.
    """
    
    try:
        if config.OPT_USE_MONGODB:
            use_mongodb()
        else:
            logger.critical("База данных не указана!")
            exit(1)
    except errors.CreationError as ex:
        logger.critical(ex)
        exit(1)

    (ok, msg) = event_loop.run_until_complete(
                    check_status(get_db()))

    if ok:
        logger.info(msg)
    else:
        logger.critical(msg)
        exit(1)

def init_sync():
    if config.OPT_SYNC:
        mods.sync(check_db_status=False)


def sync(check_db_status=True):
    """
    Начинает синхронизацию базы данных с расписанием.
    """

    logger.info("Synchronizing the data base...")

    if check_db_status:
        (ok, msg) = event_loop.run_until_complete(check_status(get_db()))
        if ok:
            logger.info("The data base is OK.")
        else:
            logger.error(
                "The data base is unavailable! Synchronizing failed.")
            return False

    schedule_parser = parser.Parser()
    
    
    (ok, msg) = event_loop.run_until_complete(
        check_status(schedule_parser))
    if ok:
        logger.info(msg)
    else:
        logger.error(msg)
        return False

    return sync_strategy.sync(parser)

def use_mongodb():
    """
    Инициализирует mongodb
    """
    global db_wrapper

    if not config.MONGODB_URL:
        logger.critical(
            "MONGODB_URL is missing! Please, define this to use mongodb.")
        exit(1)

    if not config.MONGODB_NAME:
        logger.critical(
            "MONGODB_NAME is missing! Please, define this to use mongodb.")
        exit(1)

    logger.info("Using mongodb...")
    db_wrapper = mongodb.MongoDB(url=config.MONGODB_URL,
                            name=config.MONGODB_NAME)
        

client_creation_tasks = []
def init_clients():
    if config.OPT_ALL:
        start_all()
    else:
        if config.OPT_VK:
            start_vk()
        else:
            return

    event_loop.run_until_complete(asyncio.wait(client_creation_tasks))
    logger.info("Clients has been initialized.")


def start_all():
    """ 
    Запускает всех ботов (клиентов).
    """
    start_vk()

async def do_create_client(clclass, *args, **kwargs):
    try:
        cl = clclass(*args, **kwargs)
    except CreationError as ex:
        logger.error(ex)
        return
    
    (ok, msg) = await check_status(cl)

    if ok:
        logger.info(msg)
        clcontrol.append(cl)
    else:
        logger.error(msg)


def create_client(clclass, *args, **kwargs):
    client_creation_tasks.append(do_create_client(
                clclass, *args, **kwargs))



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

    create_client(vk.VKBot, api_token=config.VK_API_TOKEN, 
                    group_id=config.VK_GROUP_ID)
    


def update():
    pass

        
def finish():
    """
    Завершает работу
    """
    logger.info("EXIT")

    tasks = []
    if db_wrapper:
        tasks.append(db_wrapper.close())

    clcontrol.close_all(tasks)
    
    event_loop = asyncio.get_event_loop()
    event_loop.run_until_complete(asyncio.wait(tasks))

