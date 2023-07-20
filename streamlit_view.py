import pymongo
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
# st.set_page_config(page_title="Geo Coding", page_icon=":rocket:", layout="wide", theme="dark")

# Connect to MongoDB server and retrieve data
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['datas']
collection = db['trail1']
data = pd.DataFrame(list(collection.find()))

st.markdown('<div style=""><h1 align="center" style="color:blue;">WELCOME TO GEO CODING</h1>', unsafe_allow_html=True)
# st.markdown("# WELCOME TO GEO CODING")
# Create a pie chart of delivery person ratings

ratings_count = data['Weatherconditions'].value_counts()
fig1, ax1 = plt.subplots()
ax1.pie(ratings_count.values, labels=ratings_count.index, autopct='%1.1f%%')
ax1.set_title('Weatherconditions')

# Create a bar chart of delivery person age
age_count = data['Road_traffic_density'].value_counts()
fig2, ax2 = plt.subplots()
colors = ['green', 'red', 'orange', 'blue']
ax2.bar(age_count.index, age_count.values, color=colors)
ax2.set_title('Road_traffic_density')
ax2.set_xlabel("Road traffic density")
ax2.set_ylabel("Count")

# Create a histogram of time taken for delivery
fig3, ax3 = plt.subplots()
ax3.hist(data['Time_taken'], bins=10)
ax3.set_title('Time Taken for Delivery')
ax3.set_xlabel("Time taken")
ax3.set_ylabel("Count")

# Aggregate query
result = collection.aggregate([
    {
        "$group": {
            "_id": "$Time_taken",
            "count": {"$sum": 1}
        }
    },
    {"$sort": {"_id": 1}}
])

# Create x-axis and y-axis data
x_axis = []
y_axis = []
for doc in result:
    x_axis.append(doc["_id"])
    y_axis.append(doc["count"])

# Create plot
fig4, ax4 = plt.subplots(figsize=(8, 6))
ax4.plot(x_axis, y_axis)

# Set labels and title
ax4.set_xlabel("Time Taken (mins)")
ax4.set_ylabel("Number of Orders")
ax4.set_title("Orders by Time Taken")

# Create a scatter plot using Matplotlib
result1 = collection.aggregate([
    {"$match": {"Weatherconditions": {"$exists": True}, "Road_traffic_density": {"$exists": True}}},
    {"$group": {"_id": {"Weather": "$Weatherconditions", "Traffic": "$Road_traffic_density"}, "Count": {"$sum": 1}}},
    {"$sort": {"Count": -1}},
    {"$group": {"_id": "$_id.Weather", "Traffic": {"$first": "$_id.Traffic"}, "Count": {"$first": "$Count"}}},
    {"$sort": {"_id": 1}}
])

df1 = pd.DataFrame(result1)

fig5, ax5 = plt.subplots()

scatter = ax5.scatter(df1["Traffic"], df1["_id"], s=df1["Count"]*10, c=df1.index, cmap='viridis')
cbar = plt.colorbar(scatter)
cbar.ax.set_ylabel('Rank', rotation=270)

ax5.set_xlabel("Road Traffic Density")
ax5.set_ylabel("Weather Condition")
ax5.set_title("Weather and Traffic Analysis")
ax5.set_xticklabels(["Low", "Medium", "High"])


# Display the graphs in Streamlit
st.pyplot(fig1)
st.pyplot(fig2)
st.pyplot(fig3)
st.pyplot(fig4)
st.pyplot(fig5)
