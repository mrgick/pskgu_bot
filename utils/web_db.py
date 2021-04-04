from config import client
db_name="DB"
#! нужен рефакторинг кода

#поиск определенного значения по ключу name
async def db_find_name(name, col="rasp"):
	collection = client[db_name][col]
	return await collection.find_one({'name': name}) 

#вывод из бд всех имен
async def do_find_all_names(name='name', col="rasp"):
	collection = client[db_name][col]
	all_names = []
	async for document in collection.find({}):
		all_names.append(document[name])
	return all_names

#вывод из бд всех имен
async def do_find_all_subs():
	collection = client[db_name]['updates']
	all_names = []
	async for document in collection.find({}):
		all_names.append({'name':document['name'],'list':document['list']})
	return all_names


#вставка user_id в бд(для рассылки)
async def do_insert_user_id(name, user_id):
	collection = client[db_name]["updates"]
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
	collection = client[db_name]["updates"]
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


#получаем, либо вставляем хеш главной страницы
async def hash_main_page(hash_page="0",insert=False):
	collection = client[db_name]["update_page"]
	data = await collection.find_one({"page":"main"})
	if data == None:
		await collection.insert_one({"page":"main"},{'hash':hash_page})
		return hash_page
	if insert:
			await collection.update_one({"page":"main"},{'$set':{'hash':hash_page}})
	else:
		hash_page=data.get('hash')
	return hash_page


updated_list_rasp = []
#вставляем в бд расписание и получаем список обновленных
async def rasp_insert(x):
    collection = client[db_name]["rasp"]
    data = await collection.find_one({"name":x.get("name")})
    if data == None:
        await collection.insert_one(x)
        updated_list_rasp.append(x.get("name"))
    else:
        if x.get("page_hash") != data.get("page_hash") or x.get("url") != data.get("url"):
            await collection.update_one({"name":x.get("name")},{'$set':{'weeks':x.get("weeks"),'page_hash':x.get("page_hash"),'url':x.get("url"),'prefix':x.get("prefix")}})
            updated_list_rasp.append(x.get("name"))