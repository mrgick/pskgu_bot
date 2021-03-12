import os
import motor.motor_asyncio

#инициалицазия mongodb
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ.get('MONGO_URL'))

#поиск определенного значения по ключу name
async def db_find_name(name, col="rasp"):
	collection = client["DB"][col]
	return await collection.find_one({'name': name}) 

#вывод из бд всех имен
async def do_find_all_names(name='name', col="rasp"):
	collection = client["DB"][col]
	all_names = []
	async for document in collection.find({}):
		all_names.append(document[name])
	return all_names

#вывод из бд всех имен
async def do_find_all_subs():
	collection = client["DB"]['updates']
	all_names = []
	async for document in collection.find({}):
		all_names.append({'name':document['name'],'list':document['list']})
	return all_names

#вставка user_id в бд(для рассылки)
async def do_insert_user_id(name, user_id):
	collection = client["DB"]["updates"]
	#создаем документ, если его нет
	data = await collection.find_one({"name":name})
	if data == None:
		await collection.insert_one({"name":name,'list':[user_id]})
		return {"name":name,'list':[user_id]}
	else:
		data = data.get('list')
		if user_id not in data:
			data.append(user_id)
			await collection.update_one({"name":name},{'$set':{'list':data}})
		return {"name":name,'list':data}

#удаление user_id из бд(для рассылки)
async def del_user_id(name, user_id):
	collection = client["DB"]["updates"]
	#проверяем есть ли документ в бд
	data = await collection.find_one({"name":name})
	if data == None:
		return {}
	else:
		data = data.get('list')
		if user_id in data:
			data.remove(user_id)
			await collection.update_one({"name":name},{'$set':{'list':data}})
		return {"name":name,'list':data}
