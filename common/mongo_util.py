import pymongo


class MongoIndex():
    
    def __init__(self, key_list, unique=False):
        self._key_list = key_list
        self._unique = unique

    def get_index(self):
        return (self._key_list, self._unique)


def ascending(key):
    return (key, pymongo.ASCENDING)


def descending(key):
    return (key, pymongo.DESCENDING)


def connect_collection(database, collection, drop=False):
    client = pymongo.MongoClient()
    db = client.get_database(database)
    if drop:
        db.drop_collection(collection)
    return db.get_collection(collection)


def create_index(collection, indexes):
    for mongoIndex in indexes:
        key_list, unique = mongoIndex.get_index()
        collection.create_index(key_list, unique=unique)
    print(list(collection.index_information()))


def insert_documents(collection, statements):
    result = collection.insert_many(statements)
    print(f"Insert {len(result.inserted_ids)} documents")


def insert_document(collection, statement):
    result = collection.insert_one(statement)
    print(result.acknowledged)
