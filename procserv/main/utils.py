import pymongo


def getDBHandle():
    client = pymongo.MongoClient("mongodb://0.0.0.0:27017/")
    DBHandle = client["erp"]
    return DBHandle