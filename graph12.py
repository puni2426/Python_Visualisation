from pymongo import MongoClient
import matplotlib.pyplot as plt
import numpy as np

client = MongoClient()
db = client.datas
orders = db.train_123

result = orders.aggregate([    { "$group": { "_id": { "type": "$Type_of_order", "city": "$City" }, "count": { "$sum": 1 } } }])

types = []
cities = []
counts = []

for doc in result:
    types.append(doc["_id"]["type"])
    cities.append(doc["_id"]["city"])
    counts.append(doc["count"])

types = np.unique(types)
cities = np.unique(cities)

data = np.zeros((len(types), len(cities)))

for i in range(len(types)):
    for j in range(len(cities)):
        for k in range(len(result)):
            if result[k]["_id"]["type"] == types[i] and result[k]["_id"]["city"] == cities[j]:
                data[i][j] = result[k]["count"]

x = np.arange(len(cities))
width = 0.35

fig, ax = plt.subplots()

for i in range(len(types)):
    ax.bar(x, data[i], width, label=types[i])

ax.set_xticks(x)
ax.set_xticklabels(cities)
ax.legend()
ax.set_xlabel("City")
ax.set_ylabel("Count")
ax.set_title("Orders by Type and City")

plt.savefig("linegraph.png")
