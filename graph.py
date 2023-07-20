from pymongo import MongoClient
import matplotlib.pyplot as plt

client = MongoClient()
db = client.datas
orders = db.train_123

result = orders.aggregate([    { "$group": { "_id": "$City", "count": { "$sum": 1 } } }])

x_axis = []
y_axis = []

for doc in result:
    x_axis.append(doc["_id"])
    y_axis.append(doc["count"])

plt.bar(x_axis, y_axis)
plt.xlabel("City")
plt.ylabel("Count")
plt.title("Orders by City")
plt.savefig("graph123.png")
