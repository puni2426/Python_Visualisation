import pymongo
import pandas_pgm as pd
import streamlit as st
import matplotlib.pyplot as plt

# Connect to MongoDB server and retrieve data
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['datas']
collection = db['trail1']
data = pd.DataFrame(list(collection.find()))

# -------------- SETTINGS --------------
page_title = "WELCOME TO GEO CODING"
page_icon = ":round_pushpin:"
layout = "centered"
# --------------------------------------

st.set_page_config(page_title=page_title, page_icon=page_icon, layout=layout)
st.title(page_title + " " + page_icon)
# st.markdown('<h1 align="center" style="color:#333652;">WELCOME TO GEO CODING</h1>', unsafe_allow_html=True)
# st.subheader(":blue[Pie Chart]")

# Dropdown
options = ["Pie Chart", "Bar Chart", "Histogram", "Line Chart", "Scatter Chart"]
selected_option = st.selectbox("Select an option", options)

# Display some text based on the user's selection
if selected_option == 'Pie Chart':
    st.write(f'You selected {selected_option}.')
    # Create a pie chart of delivery person ratings
    ratings_count = data['Weatherconditions'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(ratings_count.values, labels=ratings_count.index, autopct='%1.1f%%')

    ax1.set_title('\nPie Chart\nWeather Conditions\n', fontweight='bold', color='#DBA40E')
    st.pyplot(fig1)

elif selected_option == 'Bar Chart':
    st.write(f'You selected {selected_option}.')
    # Create a bar chart of delivery person age
    # st.subheader(":blue[Bar Chart]:bar_chart:")
    age_count = data['Road_traffic_density'].value_counts()
    fig2, ax2 = plt.subplots()
    colors = ['green', 'red', 'orange', 'blue']
    ax2.bar(age_count.index, age_count.values, color=colors)
    ax2.set_title('\nBar Chart\nRoad Traffic Density\n', fontweight='bold', color='#3D550C')
    ax2.set_xlabel("Road traffic density")
    ax2.set_ylabel("Count")
    st.pyplot(fig2)

elif selected_option == 'Histogram':
    st.write(f'You selected {selected_option}.')
    # Create a histogram of time taken for delivery
    fig3, ax3 = plt.subplots()
    ax3.hist(data['Time_taken'], bins=10)
    ax3.set_title('\nHistogram\nTime Taken for Delivery\n', fontweight='bold', color='#B10450')
    ax3.set_xlabel("Time taken")
    ax3.set_ylabel("Count")
    st.pyplot(fig3)

elif selected_option == 'Line Chart':
    st.write(f'You selected {selected_option}.')
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
    ax4.set_title("\nLine Chart\nOrders by Time Taken\n", fontweight='bold', color='#333652')
    st.pyplot(fig4)

else :
    st.write('You selected Line Chart')
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

    scatter = ax5.scatter(df1["Traffic"], df1["_id"], s=df1["Count"] * 10, c=df1.index, cmap='viridis')
    cbar = plt.colorbar(scatter)
    cbar.ax.set_ylabel('Rank', rotation=270)

    ax5.set_xlabel("Road Traffic Density")
    ax5.set_ylabel("Weather Condition")
    ax5.set_title("\nScatter Graph\nWeather and Traffic Analysis", fontweight='bold', color='#333652')
    ax5.set_xticklabels(["Low", "Medium", "High"])
    st.pyplot(fig5)

