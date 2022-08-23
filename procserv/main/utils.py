import sys
import pymongo
from pprint import pprint


def get_db_handle():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db_handle = client["erp"]
    return db_handle


def show_mongo(db_handle, col):
    col_handle = db_handle[col]
    i = 0
    for item in col_handle.find():
        pprint(item)
        i += 1
    print()


def count_mongo(db_handle, col):
    col_handle = db_handle[col]
    print(col, len(list(col_handle.find({'sent': 0}))))


def clear_mongo(db_handle, col):
    col_handle = db_handle[col]
    del_obj = col_handle.delete_many({})
    print(f'deleted {del_obj.deleted_count} objects of type {col}')


if __name__ == '__main__':

    if len(sys.argv) == 2:
        db_handle = get_db_handle()
        if sys.argv[1] == 'show':
            show_mongo(db_handle, 'category')
            show_mongo(db_handle, 'measure_unit')
            # show_mongo(db_handle, 'product')
        elif sys.argv[1] == 'clear':
            clear_mongo(db_handle, 'category')
            clear_mongo(db_handle, 'measure_unit')
            clear_mongo(db_handle, 'product')
        elif sys.argv[1] == 'count':
            count_mongo(db_handle, 'category')
            count_mongo(db_handle, 'measure_unit')
            count_mongo(db_handle, 'product')
    else:
        print("provide correct command line argument")

    