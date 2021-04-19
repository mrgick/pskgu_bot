
import optparse
import logging
import colorlog
import config 
import mods
import sys
import atexit
 
# import asyncio
# from utils.storage import initialize_storage
# from utils.parser import parser
# from blueprints import (
# 	begin_and_help_router,
# 	week_router,
# 	map_router,
# 	subscription_router
# )
# from config import bot

"""
TODO:
-переделать /help
-переделать парсер (рефакторинг)
-переделать бд и вставку нового
-добавить ical
-сделать тесты
"""



#наши роутеры(события)
# bot.dispatcher.add_router(subscription_router)
# bot.dispatcher.add_router(week_router)
# bot.dispatcher.add_router(map_router)
# bot.dispatcher.add_router(begin_and_help_router)

usage = ("Usage: %s" % config.LAUNCH_SH
        if config.LAUNCH_SH else "Usage: %prog") + " [OPTIONS]"

optparser = optparse.OptionParser(usage=usage)


optparser.add_option("", "--version", action="store_true",
        help="Показать версию и выйти.")

optparser.add_option("-s", "--sync", action="store_true",
        help="Начать синхронизацию базы данных с расписанием.")

optparser.add_option("", "--use-mongodb", action="store_true",
        help="Использовать mongodb в качестве базы данных.")

optparser.add_option("", "--vk", action="store_true",
        help="Запустить VK бота.")

optparser.add_option("-a", "--all", action="store_true",
        help="Запустить всех ботов (клиентов).")

optparser.add_option("-x", "--shell", action="store_true",
        help="Войти в оболочку после инициализации всех компонентов.")

SHOW_ONLY_VERSION = False

def process_args(opts, args):

    global SHOW_ONLY_VERSION
    SHOW_ONLY_VERSION = opts.version

    config.OPT_SYNC = opts.sync

    config.OPT_ALL = opts.all

    config.OPT_USE_MONGODB = opts.use_mongodb

    config.OPT_VK = opts.vk

def init_logging():

    color_formatter = colorlog.ColoredFormatter(
        "%(log_color)s [%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%a %d %b %Y %H:%M:%S"
    )
    file_formatter = logging.Formatter(
        "[%(asctime)s] %(levelname)s: %(message)s",
            datefmt="%a %d %b %Y %H:%M:%S"
    )


    stream_handler = logging.StreamHandler(sys.stderr)
    stream_handler.setFormatter(color_formatter)

    file_handler = logging.FileHandler(config.LOGFILE)
    file_handler.setFormatter(file_formatter)

    pskgu_bot_logger = logging.getLogger(config.PSKGU_BOT_LOGGER)
    pskgu_bot_logger.setLevel(logging.INFO)
    pskgu_bot_logger.addHandler(stream_handler)
    pskgu_bot_logger.addHandler(file_handler)


    debug_logger = logging.getLogger(config.DEBUG_LOGGER)
    debug_logger.setLevel(logging.DEBUG)
    debug_logger.propagate = False
    if config.DEBUG:
        debug_logger.addHandler(stream_handler)
        debug_logger.addHandler(file_handler)

    
def show_version():
    version_str = "PSKGU bot. Version %s" % config.VERSION 
    if SHOW_ONLY_VERSION:
        print(version_str)
        exit(0)
    logging.getLogger(config.PSKGU_BOT_LOGGER).info(version_str)
        

def main():

    atexit.register(mods.finish)

    (opts, args) = optparser.parse_args()
    process_args(opts, args)

    init_logging()

    show_version()
    
    mods.init()

    mods.update()

    exit(0)

if __name__ == "__main__":
    main()
