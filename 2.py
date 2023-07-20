# import pymongo
# import matplotlib.pyplot as plt
#
#
# # connect to MongoDB
# client = pymongo.MongoClient("mongodb://localhost:27017/")
# db = client.employee
# collection = db.emp
#
# # retrieve data from collection
# data = collection.find({}, {'_id': 0, 'DEPARTMENT_ID': 1, 'SALARY': 1})
#
# # create lists for x and y axis data
# x_data = []
# y_data = []
# for item in data:
#     x_data.append(item['DEPARTMENT_ID'])
#     y_data.append(item['SALARY'])
#
# # create bar chart
# plt.bar(x_data, y_data)
# plt.show()
import pymongo
import matplotlib.pyplot as plt


# connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["datas"]
# collection = db.train1

# retrieve data from collection
#data = collection.find({}, {'_id': 0, 'Weatherconditions': 1, 'Time_taken(min)': 1})
# x=db.train_123.aggregate([{'$match':{'$Order_Date':''}},{'$group':{'_id':'$City', 'Total_Count':{'$':'$Road_traffic_density'}}}])
x=db.train_123.aggregate({"$group":{"_id":"$City","count":{"$sum":1}}})
x_data = []
y_data = []
for item in x:
    x_data.append(item['_id'])
    y_data.append(item['count'])

# create bar chart
    plt.bar(x_data, y_data)
# plt.xlabel("Weatherconditions")
# plt.ylabel("Time_taken(min)")
plt.savefig("new_bar.png")

# db.train_123.aggregate([ Order_Date: {$gte: ISODate("2022-01-01T00:00:00Z"),$lte: ISODate("2022-01-31T23:59:59Z")},{$group:{_id:"$City",count:{$sum:1}}}])