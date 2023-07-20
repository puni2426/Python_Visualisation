import pymongo
from pprint import pprint
from uuid import uuid1
import json
# client = pymongo.MongoClient("mongodb://localhost:27017/")
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Bank"]
collection = db["t1"]
print("\n-------------------------WELCOME-------------------------")
print("Current Database is :", db.name)
print("\nCollections are:")
print(db.list_collection_names())
print()
# collection.insert_one({"name":input(),"amount":int(input()),"status":bool(input()),"tansaction_id":str(uuid1())})
# for i in collection.find({"FIRST_NAME": {"$regex": "a"}}, {"FIRST_NAME": 1}).sort("FIRST_NAME", pymongo.ASCENDING):
#     pprint(i)
def add():
    no = int(input("how many students details you need to store in database:"))
    for i in range(no):
            name = input("Enter your name :")
            amount = input("Enter your amount :")
            status = bool(input("Enter your Status (t/f) :"))
            # tansaction_id: str(uuid1())
            document = {"name":name,"amount":amount,"status":status,"tansaction_id":str(uuid1())}
            collection.insert_one(document)
def prints():
    count = collection.count_documents({})
    print("Total number of documents :", count,end="\n\n")
    for i in collection.find():
            pprint(i, indent=4)
            print()
def seach():
    se =input("enter name to search")
    query = {"name":{"$regex":se}}
    C = collection.count_documents(query)
    print("Total number of matching documents :", C, end="\n\n")
    for i in collection.find(query):
        pprint(i, indent=4)
        print()
    else:
        print("Please try with other names")
def updat():
    se = input("enter name to update")
    newName = input("Enter new name to update")
    filter = {"name":se}
    update = {"$set":{"name":newName}}
    collection.update_many(filter,update)
def delete():
    se = input("Enter name to delete ")
    query  = {"name":{"$regex":se}}
    if collection.find(query):
        collection.delete_one(query)
        print("Deleted Successfully!!!")
    else:
        print("Data Not Found!!!")
while 1:
        CH = int(input("Enter your choice\n 1. print details\n 2. update\n 3. search\n 4. add user\n 5. delete User\n 6. delete Collection\n"))
        if CH == 1:
                prints()
        elif CH == 2:
                updat()
        elif CH == 3:
                seach()
        elif CH == 4:
                add()
        elif CH == 5:
                delete()
        elif CH ==6:
                collection.drop()
        elif CH == 7:
                print(db.list_collection_names())
        else:
            exit("Thankyou!")