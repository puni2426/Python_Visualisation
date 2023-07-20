import pymongo
import matplotlib.pyplot as plt

# Connect to MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["datas"]
collection = db["trail1"]

# Aggregate the data and rank by time taken
pipeline = [
    {"$match": {"Weatherconditions": {"$exists": True}, "Road_traffic_density": {"$exists": True}}},
    {"$group": {"_id": {"Weather": "$Weatherconditions", "Traffic": "$Road_traffic_density"},
                "Avg_time_taken": {"$avg": "$Time_taken"}}},
    {"$sort": {"Avg_time_taken": 1}}
]

result = collection.aggregate(pipeline)

# Retrieve data from the aggregation result
x_values = []
y_values = []
ranks = []
for i, doc in enumerate(result):
    x_values.append(doc["_id"]["Traffic"])
    y_values.append(doc["Avg_time_taken"])
    ranks.append(i+1)

# Create a scatter plot with rank
plt.scatter(ranks, y_values)
plt.xlabel("Rank")
plt.ylabel("Average Time Taken")
plt.title("Delivery Time vs Traffic Density with Rank")

# Display the plot
plt.show()
