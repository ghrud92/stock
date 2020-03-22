import pymongo

import mongo_util
from mongo_util import MongoIndex, ascending, descending
import stock_util

DATA_PATH = "data/naver_statements.json"

STATEMENT_COLLECTION_INDEX = [
    MongoIndex([ascending('sid')], True),
    MongoIndex([ascending('company')]),
    MongoIndex([descending('term'), descending('year')]),
    MongoIndex([descending('term'), descending('year'), descending('month')])
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


if __name__ == "__main__":
    data = stock_util.load_json(DATA_PATH)
    statements = [distribute_finance(statement) for statement in data]
    statements = [item for sublist in statements for item in sublist]

    collection = mongo_util.connect_collection('stock', 'statement', True)
    mongo_util.create_index(collection, STATEMENT_COLLECTION_INDEX)
    mongo_util.insert_documents(collection, statements)
