from os import environ as env
import time

# from vkwave.bots import SimpleLongPollBot
# import motor.motor_asyncio

#инициализация бота
#bot = SimpleLongPollBot(tokens=env.get("VK_TOKEN"), group_id = env.get("VK_GROUP_ID")) #инициалицазия mongodb
#client = motor.motor_asyncio.AsyncIOMotorClient(env.get("MONGODB_URL"))
# сайт с расписанием


VK_API_TOKEN = env.get("VK_API_TOKEN")
VK_GROUP_ID = env.get("VK_GROUP_ID")

SCHEDULE_URL = env.get("SCHEDULE_URL") 


MONGODB_URL = env.get("MONGODB_URL")
MONGODB_NAME = env.get("MONGODB_NAME")

LAUNCH_SH = env.get("LAUNCH_SH")

START_TIME = time.time()

LOGFILE = env.get("LOGFILE")

PSKGU_BOT_LOGGER = "pskgu-bot"
DEBUG_LOGGER = "pskgu-bot-DEBUG"

VERSION_MAJOR = int(env.get("VERSION_MAJOR")) 
VERSION_MINOR = int(env.get("VERSION_MINOR"))

VERSION = "%i.%02i" % (VERSION_MAJOR, VERSION_MINOR)

DEBUG = env.get("DEBUG").lower().strip()
DEBUG = (DEBUG == "1" or DEBUG == "true")

# Синхронизировать базу с текущим расписанием
OPT_SYNC = False

# Использовать mongodb
OPT_USE_MONGODB = False

# Использовать ВК-бота
OPT_VK = False


