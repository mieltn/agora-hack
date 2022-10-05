import pymongo


def getDBHandle():
    # for localhost use 'localhost' instead of the name of the service from docker-compose.yml
    client = pymongo.MongoClient("mongodb://mongo:27017/")
    DBHandle = client["erp"]
    return DBHandle