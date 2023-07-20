from pymongo import MongoClient
import matplotlib.pyplot as plt
import pandas_pgm as pd
import streamlit as st

client = MongoClient()
db = client.datas
orders = db.trail1

result = orders.aggregate([
    {"$match": {"Weatherconditions": {"$exists": True}, "Road_traffic_density": {"$exists": True}}},
    {"$group": {"_id": {"Weather": "$Weatherconditions", "Traffic": "$Road_traffic_density"}, "Count": {"$sum": 1}}},
    {"$sort": {"Count": -1}},
    {"$group": {"_id": "$_id.Weather", "Traffic": {"$first": "$_id.Traffic"}, "Count": {"$first": "$Count"}}},
    {"$sort": {"_id": 1}}
])

df = pd.DataFrame(result)

fig, ax = plt.subplots()

scatter = ax.scatter(df["Traffic"], df["_id"], s=df["Count"]*10, c=df.index, cmap='viridis')
cbar = plt.colorbar(scatter)
cbar.ax.set_ylabel('Rank', rotation=270)

ax.set_xlabel("Road Traffic Density")
ax.set_ylabel("Weather Condition")
ax.set_title("Weather and Traffic Analysis")
ax.set_xticklabels(["Low", "Medium", "High"])

st.pyplot(fig)
