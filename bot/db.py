import os
import motor.motor_asyncio

#инициалицазия mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGO_URL'))

#поиск определенного значения по ключу name
async def db_find_name(name):
	db = client["DB"]
	collection = db["rasp"]
	values = await collection.find_one({'name': name})
	return values 

#вывод из бд всех имен
async def do_find_all_names():
	db = client["DB"]
	collection = db["rasp"]
	all_names=[]
	async for document in collection.find({}):
		all_names.append(document['name'])
	return all_names