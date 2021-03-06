from config import mongo_url
import pymongo

def insert_document(collection, data, multiple=False):
	""" Function to insert single or multiple documents into a collection and
	return the document's id.
	"""
	#structure {'name':key,'text':value,'hash':'f5c53844c0b362d5ae3dc44b38001673'}
	if multiple:
		return collection.insert_many(data).inserted_ids
	else:
		return collection.insert_one(data).inserted_id


def find_document(collection, elements, multiple=False):
	""" Function to retrieve single or multiple documents from a provided
	Collection using a dictionary containing a document's elements.
	"""
	if multiple:
		results = collection.find(elements)
		return [r for r in results]
	else:
		return collection.find_one(elements)

def update_document(collection, query_elements, new_values):
	""" Function to update a single document in a collection.
	"""
	collection.update_one(query_elements, {'$set': new_values})
	return 'updated'

def db_work():
	""" working with mongodb
	"""

	try:
		# Create the client
		client = pymongo.MongoClient(mongo_url)
		# Connect to our database
		db = client['DB']
		# Choose collection
		collection = db['rasp']


		#log=test.main()
		#for key,value in log.items():
		#	arr_insert.append({'name':key,'text':value,'hash':'f5c53844c0b362d5ae3dc44b38001673'})
		#print(arr_insert)
		#insert_document(series_collection, arr_insert,multiple=True)
		print(find_document(collection,{'name':'0431-06'}))
		print(update_document(collection,{'name':'0431-06'},{'hash':'1'}))
		print(find_document(collection,{'name':'0431-06'},True)[0]['hash'])


	except pymongo.errors as e:
		print(e)

	finally:
		#close the connection
		client.close()


if __name__ == "__main__":
	db_work()