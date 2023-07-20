# import pymongo
# client = pymongo.MongoClient()
# db = client['myDB']
# collection = db['mytable']
# collection.insert_one({'Name':'Punith'})
# print("Inserted Successfully")
# # db.drop_collection('mytable')



import re
p="^[A-Za-z0-9._]+[@][a-zA-Z0-9]+[.][A-Za-z]{2,3}$"
s=["All@gamil.com","Zxc@qws.qes123","asd@qwe.zx"]
for i in s:
    x=re.match(p,i)
    if x:
        print(i)