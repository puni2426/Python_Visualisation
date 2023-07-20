import matplotlib.pyplot as plt
from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient()
db = client.datas
collection = db.trail1

pipeline = [    {"$group": {"_id": "$Type_of_vehicle", "Time_taken": {"$push": "$Time_taken"}}}]

result = list(db.trail1.aggregate(pipeline))

data = [r["Time_taken"] for r in result]
labels = [r["_id"] for r in result]

plt.boxplot(data, labels=labels)
plt.title("Delivery Time by Vehicle Type")
plt.xlabel("Vehicle Type")
plt.ylabel("Time Taken (min)")
plt.show()

