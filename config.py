import os
from vkwave.bots import SimpleLongPollBot
import motor.motor_asyncio
#инициализация бота
bot = SimpleLongPollBot(tokens=os.environ.get('TOKEN_VK'), group_id = os.environ.get('GROUP_ID'))
#инициалицазия mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGO_URL'))
# сайт с расписанием
REMOTE_URL = "http://rasp.pskgu.ru"