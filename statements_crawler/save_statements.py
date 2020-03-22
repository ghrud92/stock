import pymongo

import stock_util

DATA_PATH = "data/naver_statements.json"

STATEMENT_COLLECTION_INDEX = [
    {'key': [('sid', pymongo.ASCENDING)], 'unique': True},
    {'key': [('company', pymongo.ASCENDING)], 'unique': False},
    {'key': [('term', pymongo.DESCENDING), ('year', pymongo.DESCENDING)], 
    'unique': False},
    {'key': [('term', pymongo.DESCENDING), ('year', pymongo.DESCENDING), 
    ('month', pymongo.DESCENDING)], 'unique': False}
]


def distribute_finance(data):
    code = data['code']
    company = data['company']
    finances = data['finance']
    result = []
    for finance in finances:
        if not finance['date']:
            continue
        
        consensus = False
        if "(E)" in finance['date']:
            consensus = True
            finance['date'] = finance['date'].replace("(E)", "")
        year = int(finance['date'][:4])
        month = int(finance['date'][-2:])
        finance.pop('date', None)

        finance['sid'] = f"{code}_{finance['term']}_{year}_{month}"
        finance['code'] = code
        finance['company'] = company
        finance['year'] = year
        finance['month'] = month
        finance['consensus'] = consensus

        finance = stock_util.convert_statement_types(finance)
        result.append(finance)
    return result


def insert_documents(statements):
    collection = connect_collection(db='stock', collection='statement', drop=True)
    create_index(collection, STATEMENT_COLLECTION_INDEX)
    result = collection.insert_many(statements)
    print(f"Insert {len(result.inserted_ids)} documents")


def insert_document(statement):
    collection = connect_collection(db='stock', collection='statement', drop=True)
    create_index(collection, STATEMENT_COLLECTION_INDEX)
    print(f"insert {statement['sid']} document.")
    result = collection.insert_one(statement)
    print(result.acknowledged)


def connect_collection(db, collection, drop=False):
    client = pymongo.MongoClient()
    db = client.get_database(db)
    if drop:
        db.drop_collection(collection)
    return db.get_collection(collection)


def create_index(collection, indexes):
    for index in indexes:
        collection.create_index(index['key'], unique=index['unique'])


if __name__ == "__main__":
    data = stock_util.load_json(DATA_PATH)
    statements = [distribute_finance(statement) for statement in data]
    statements = [item for sublist in statements for item in sublist]
    insert_documents(statements)
