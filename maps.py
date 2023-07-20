import pymongo
client = pymongo.MongoClient()
db = client["database"]
col = db["collection"]
col.insert_one({"name":"hello"})
# client.drop_database("Newdatabase")
x = client.list_database_names()
print("Database names:")
for i in x:
    print(i)

y = db.list_collection_names()
print("\nCollections in database:")
for i in y:
    print(i)

cnt = col.count_documents({})
print("Number of documents in emp collection :",cnt)
