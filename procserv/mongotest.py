import pymongo

def insert():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]

    mydict = { "name": "John", "address": "Highway 37" }

    x = mycol.insert_one(mydict)

    return x


def find():
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mydatabase"]
    mycol = mydb["customers"]

    myquery = { "address": "Highway 37" }

    mydoc = mycol.find(myquery)

    return mydoc


def main():
    insert()
    doc = find()
    for x in doc:
        print(x)
    # print(doc)


if __name__ == "__main__":
    main()

