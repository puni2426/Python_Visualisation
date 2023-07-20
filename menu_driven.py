import pymongo
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas_pgm as pd
import folium
from folium import Popup

# create a MongoClient object and connect to the running MongoDB instance
client = pymongo.MongoClient()
print("Connection Established Successfully")
# creating a database
db = client['datas']
print("Database created.")
# creating a collections
collection = db['trail1']
collection1 = db['p2']
print("Collection Created")


# open the CSV file
def push_data():
    with open('/home/ee212821/Downloads/Dataset1.csv') as f:
        # create a CSV reader object
        reader = csv.DictReader(f)
        # read the data from the file into a list of dictionaries
        data = [dict(row) for row in reader]
    # insert the data into the collection
    result = collection1.insert_many(data)
    print("Documents Inserted")


def histogram1():
    # group the data based on the "Time_taken" field and count the occurrences
    pipeline = [
        {"$group": {"_id": "$Time_taken", "count": {"$sum": 1}}}
    ]
    result = list(collection.aggregate(pipeline))
    # create a list of counts and a list of corresponding values
    counts = [r["count"] for r in result]
    values = [r["_id"] for r in result]
    # plot the histogram using matplotlib
    # weights for yaxis, bins helps to
    plt.hist(values, weights=counts, bins=20)
    plt.xlabel("Time Taken")
    plt.ylabel("Count")
    plt.title("Histogram of Delivery Time Taken")
    plt.savefig("hist1.png")
    plt.show()
    print("Histogram plotted and saved")


def histogram2():
    # group the data based on the "Delivery person age" field and count the occurrences
    pipeline = [{"$group": {"_id": None, "Delivery_person_Age": {"$push": "$Delivery_person_Age"}}}]
    results = collection.aggregate(pipeline)
    x_axis = []
    for i in results:
        x_axis.append(i['Delivery_person_Age'])
    # Create and display the histogram graph
    plt.hist(x_axis, bins=20)
    plt.title('Histogram of Delivery person Age')
    plt.xlabel('Delivery person Age')
    plt.ylabel('Frequency')
    plt.savefig("hist2.png")
    plt.show()
    print("Histogram plotted and saved")


def bar_graph1():
    # Aggregate data of "Road Traffic Density" and "City" with respect to "Delivery Person Rating"
    pipeline = [
        {"$group": {"_id": {"City": "$City", "Road_traffic_density": "$Road_traffic_density"},
                    "Delivery_person_Ratings": {"$avg": "$Delivery_person_Ratings"}}},
        {"$sort": {"_id.City": 1, "_id.Road_traffic_density": 1, "Delivery_person_Ratings": 1}}
    ]

    result = list(collection.aggregate(pipeline))
    # Create dataframe
    df = pd.DataFrame(result)
    df[['City', 'Road_traffic_density']] = pd.DataFrame(df['_id'].tolist())
    df = df.drop(['_id'], axis=1)
    df = df.pivot(index='City', columns='Road_traffic_density', values='Delivery_person_Ratings')
    # Create bar chart
    df.plot(kind='bar')
    plt.xlabel('City')
    plt.ylabel('Delivery person Ratings')
    plt.title('Traffic Density with respect to City and Delivery Rating Achieved')
    plt.legend(loc='upper right')
    plt.savefig('Bar1.png')
    plt.show()
    print("Bar Graph plotted and saved")


def bar_graph2():
    # Selecting the data based on "delivery Person Rating" and "Delivery Person Age"
    data = list(collection.find({}, {"Delivery_person_Ratings": 1, "Delivery_person_Age": 1, "_id": 0}))
    x_axis = [d["Delivery_person_Ratings"] for d in data]
    y_axis = [d["Delivery_person_Age"] for d in data]
    # plot data
    plt.bar(sorted(y_axis), sorted(x_axis), color='maroon', width=0.08)
    plt.ylabel("Delivery person ratings")
    plt.xlabel("Delivery person age")
    plt.title("Delivery Person Rating with respect to Delivery Person Age")
    plt.savefig('Bar2.png')
    plt.show()
    print("Bar Graph plotted and saved")


def bar_graph3():
    # Aggregating the data based on "Road traffic density" count
    result = collection.aggregate(
        [{"$group": {"_id": "$Road_traffic_density", "count": {"$sum": 1}}}, {"$sort": {"count": -1}}])
    x_axis = []
    y_axis = []
    for doc in result:
        x_axis.append(doc["_id"])
        y_axis.append(doc["count"])
    colors = ['g', 'r', 'y', 'orange']
    plt.bar(x_axis, y_axis, color=colors)
    plt.xlabel("Road traffic density")
    plt.ylabel("Count")
    plt.title("Orders by Road traffic density")
    plt.savefig('Bar3.png')
    plt.show()
    print("Bar Graph plotted and saved")


def line_chart():
    # Aggregating the data based on "Time taken" with respect to number of "orders delivered" count
    result = collection.aggregate([{"$group": {"_id": "$Time_taken", "count": {"$sum": 1}}}, {"$sort": {"_id": 1}}])
    x_axis = []
    y_axis = []
    for doc in result:
        x_axis.append(doc["_id"])
        y_axis.append(doc["count"])
    plt.plot(x_axis, y_axis, color='red', marker='o', markerfacecolor='blue', fillstyle='full', alpha=0.5)
    plt.xlabel("Time Taken")
    plt.ylabel("Count")
    plt.title("Order by Time taken")
    plt.savefig('line1.png')
    plt.show()
    print("Line Chart plotted and saved")


def pie_chart1():
    # retrieve data from collection based on "Type of Order"
    result = collection.aggregate([{"$group": {"_id": "$Type_of_order", "count": {"$sum": 1}}}])
    labels = []
    sizes = []
    for doc in result:
        labels.append(doc["_id"])
        sizes.append(doc["count"])
    plt.pie(sizes, labels=labels, autopct='%.2f%%', startangle=90)
    plt.title("Orders by Type")
    plt.axis("equal")
    plt.legend(loc='upper right')
    plt.savefig('Pie1.png')
    plt.show()
    print("Pie Chart plotted and saved")


def pie_chart2():
    # Aggregating the data based on "Weather-condition"
    result = collection.aggregate([{"$group": {"_id": "$Weatherconditions", "count": {"$sum": 1}}}])
    labels = []
    sizes = []
    for doc in result:
        labels.append(doc["_id"])
        sizes.append(doc["count"])
    plt.pie(sizes, labels=labels, autopct="%.1f%%", startangle=90)
    plt.title("Weatherconditions")
    plt.axis("equal")
    plt.savefig('Pie2.png')
    plt.show()
    print("Pie Chart plotted and saved")


def pie_chart3():
    # Aggregating the data based on "Delivery Person Age"
    result = collection.aggregate(
        [{"$group": {"_id": "$Delivery_person_Age", "count": {"$sum": 1}}}, {"$sort": {"_id": 1}}])
    labels = []
    sizes = []
    for doc in result:
        labels.append(doc["_id"])
        sizes.append(doc["count"])
    plt.pie(sizes, labels=labels, autopct="%.1f%%", startangle=90)
    plt.title("Delivery person Age")
    plt.axis("equal")
    plt.savefig('Pie3.png')
    plt.show()
    print("Pie Chart plotted and saved")


def scatter_chart1():
    # Aggregation based on grouping with "Weather-condition" and "Road Traffic Density"
    result = collection.aggregate([{"$group": {
        "_id": {"weather": "$Weatherconditions", "traffic": "$Road_traffic_density"}, "count": {"$sum": 1}}}])
    x_axis = []
    y_axis = []
    sizes = []
    for doc in result:
        y_axis.append(doc["_id"]["weather"])
        x_axis.append(doc["_id"]["traffic"])
        sizes.append(doc["count"])
    plt.scatter(x_axis, y_axis, s=sizes, edgecolors='purple', color='cyan')
    plt.xlabel("Weather Conditions")
    plt.ylabel("Road Traffic Density")
    plt.title("Orders by Weather and Traffic")
    plt.savefig('scatter1.png')
    plt.show()
    print("Scatter Chart plotted and saved")


def scatter_chart2():
    # Aggregation Pipeline : the data mapping done by "Weather-condition" and "Road Traffic Density",
    # grouping performed with mapped data with "average time taken" to deliver the order
    pipeline = [
        {"$match": {"Weatherconditions": {"$exists": True}, "Road_traffic_density": {"$exists": True}}},
        {"$group": {"_id": {"Weather": "$Weatherconditions", "Traffic": "$Road_traffic_density"},
                    "Avg_time_taken": {"$avg": "$Time_taken"}}},
        {"$sort": {"Avg_time_taken": 1}}
    ]
    result = collection.aggregate(pipeline)
    print(result)
    # Retrieve data from the aggregation result
    x_values = []
    y_values = []
    ranks = []
    for i, doc in enumerate(result):
        x_values.append(doc["_id"]["Traffic"])
        y_values.append(doc["Avg_time_taken"])
        ranks.append(i + 1)
    # Create a scatter plot with rank
    colors = np.random.rand(25)
    plt.scatter(ranks, y_values, c=colors)
    plt.xlabel("Rank")
    plt.ylabel("Average Time Taken")
    plt.title("Delivery Time vs Traffic Density with Rank")
    # Display the plot
    plt.savefig('scatter1.png')
    plt.show()
    print("Scatter Chart plotted and saved")


def box():
    # Median, Quartiles, Whiskers, outliers
    # grouping based on "Type of Vehicle" and "Time taken"
    pipeline = [{"$group": {"_id": "$Weatherconditions", "Time_taken": {"$push": "$Time_taken"}}}]
    # Execute aggregation pipeline
    result = list(collection.aggregate(pipeline))
    # Extract data and labels from result
    data = [r["Time_taken"] for r in result]
    labels = [r["_id"] for r in result]
    # Plot boxplot
    plt.boxplot(data, labels=labels)
    plt.title("Delivery Time by Vehicle Type")
    plt.xlabel("Weatherconditions")
    plt.ylabel("Time Taken")
    plt.savefig('box.png')
    plt.show()
    print("Box plotted and saved")


def geo_map():
    # Plotting the Restaurant and Delivery locations on map
    # Create a Folium map object centered on the mean of the latitude and longitude columns
    # if needed use , tiles='Stamenterrain'
    my_map = folium.Map(location=[22.77710235, 75.8961588], zoom_start=10)

    # Retrieve data from MongoDB and add markers to the map
    for doc in collection.find():
        restaurant_lat = doc['Restaurant_latitude']
        restaurant_lon = doc['Restaurant_longitude']
        delivery_lat = doc['Delivery_location_latitude']
        delivery_lon = doc['Delivery_location_longitude']
        Restaurant_popup = f"<strong>Restaurant latitude</strong>: {restaurant_lat}<br><strong>Restaurant longitude</strong>: {restaurant_lon}<br><strong>Delivery Person ID</strong>: {doc['Delivery_person_ID']}<br>"
        restaurant_marker = folium.Marker(location=[restaurant_lat, restaurant_lon], tooltip="Restaurant Location",
                                          icon=folium.Icon(color='purple', icon='star'),
                                          popup=Popup(Restaurant_popup, max_width=250, min_width=150, max_height=150))
        restaurant_marker.add_to(my_map)
        Delivery_popup = f"<strong>Delivery latitude</strong>: {delivery_lat}<br><strong>Delivery longitude</strong>: {delivery_lon}<br><strong>Type of Order</strong>: {doc['Type_of_order']}<br><br><strong>Delivery Rating</strong>: {doc['Delivery_person_Ratings']}"
        delivery_marker = folium.Marker(location=[delivery_lat, delivery_lon], tooltip="Delivery Location",
                                        icon=folium.Icon(color='red', icon='home'),
                                        popup=Popup(Delivery_popup, max_width=250, min_width=150, max_height=150))
        delivery_marker.add_to(my_map)

    # Display the map
    my_map.save('geoMap.html')
    # my_map.show_in_browser()
    print("Map plotted and saved")


def geo_map1():
    # mapping the "Restaurant" and "Delivery Location"
    first_doc = collection.find_one()
    my_map = folium.Map(location=[first_doc['Restaurant_latitude'], first_doc['Restaurant_longitude']], zoom_start=10)

    # Retrieve data from MongoDB and add markers to the map
    for doc in collection.find():
        restaurant_lat = doc['Restaurant_latitude']
        restaurant_lon = doc['Restaurant_longitude']
        delivery_lat = doc['Delivery_location_latitude']
        delivery_lon = doc['Delivery_location_longitude']
        Restaurant_popup = f"<strong>Restaurant latitude</strong>: {restaurant_lat}<br><strong>Restaurant longitude</strong>: {restaurant_lon}<br><strong>Delivery Person ID</strong>: {doc['Delivery_person_ID']}<br>"
        restaurant_marker = folium.Marker(location=[restaurant_lat, restaurant_lon], tooltip="Restaurant Location",
                                          icon=folium.Icon(color='purple', icon='star'),
                                          popup=Popup(Restaurant_popup, max_width=250, min_width=150, max_height=150))
        restaurant_marker.add_to(my_map)
        Delivery_popup = f"<strong>Delivery latitude</strong>: {delivery_lat}<br><strong>Delivery longitude</strong>: {delivery_lon}<br><strong>Delivery Rating</strong>: {doc['Delivery_person_Ratings']}<br>"
        delivery_marker = folium.Marker(location=[delivery_lat, delivery_lon], tooltip="Delivery Location",
                                        icon=folium.Icon(color='red', icon='home'),
                                        popup=Popup(Delivery_popup, max_width=250, min_width=150, max_height=150))
        delivery_marker.add_to(my_map)
        folium.PolyLine(locations=[(restaurant_lat, restaurant_lon), (delivery_lat, delivery_lon)], color='#69b3a2',
                        weight=2).add_to(my_map)
    # Display the map
    my_map.save('geoMap1.html')
    # my_map.show_in_browser()
    print("Map plotted and saved")


def geo_map2():
    # selecting one particular document for mapping the "Restaurant" and "Delivery Location"
    doc = collection.find_one()
    restaurant_lat = doc['Restaurant_latitude']
    restaurant_lon = doc['Restaurant_longitude']
    delivery_lat = doc['Delivery_location_latitude']
    delivery_lon = doc['Delivery_location_longitude']
    my_map = folium.Map(location=[restaurant_lat, restaurant_lon], zoom_start=10)
    Restaurant_popup = f"<strong>Restaurant latitude</strong>: {restaurant_lat}<br><strong>Restaurant longitude</strong>: {restaurant_lon}<br><strong>Delivery Person ID</strong>: {doc['Delivery_person_ID']}<br><strong>Time Ordered</strong>: {doc['Time_Orderd']}<br>"
    restaurant_marker = folium.Marker(location=[restaurant_lat, restaurant_lon], tooltip="Restaurant Location",
                                      icon=folium.Icon(color='purple', icon='star'),
                                      popup=Popup(Restaurant_popup, max_width=250, min_width=150, max_height=150))
    restaurant_marker.add_to(my_map)
    Delivery_popup = f"<strong>Delivery latitude</strong>: {delivery_lat}<br><strong>Delivery longitude</strong>: {delivery_lon}<br><strong>Type of Order</strong>: {doc['Type_of_order']}<br><strong>Time Taken</strong>: {doc['Time_taken']}<br><strong>Delivery Rating</strong>: {doc['Delivery_person_Ratings']}<br>"
    delivery_marker = folium.Marker(location=[delivery_lat, delivery_lon], tooltip="Delivery Location",
                                    icon=folium.Icon(color='red', icon='home'),
                                    popup=Popup(Delivery_popup, max_width=250, min_width=150, max_height=150))
    delivery_marker.add_to(my_map)
    folium.PolyLine(locations=[(restaurant_lat, restaurant_lon), (delivery_lat, delivery_lon)], color='#69b3a2',
                    weight=2).add_to(my_map)
    # Display the map
    my_map.save('geoMap2.html')
    # my_map.show_in_browser()
    print("Map plotted and saved")


if __name__ == '__main__':
    print("-------------------------Welcome to Geo Coding------------------------")
    while True:
        print(
            "1. Push Data\n2. Histogram\n3. Bar Chart\n4. Line Chart\n5. Pie Chart\n6. Scatter Chart\n7. Box Plot\n8. Geo Map")
        ch = int(input("Enter your choice: \n"))
        if ch == 1:
            push_data()
        elif ch == 2:
            while True:
                print("Histogram Available: ")
                print("A. Histogram of Delivery Time Taken")
                print("B. Delivery Person Rating with respect to Delivery Person Age")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    histogram1()
                elif choice == 'B':
                    histogram2()
                else:
                    print("Invalid option")
                    break
        elif ch == 3:
            while True:
                print("Bar Graphs Available: ")
                print("A. Traffic Density with respect to City and Delivery Rating Achieved")
                print("B. Delivery Person Rating with respect to Delivery Person Age")
                print("C. Number of Orders with respect to City")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    bar_graph1()
                elif choice == 'B':
                    bar_graph2()
                elif choice == 'C':
                    bar_graph3()
                else:
                    print("Invalid Bar Graph option")
                    break
        elif ch == 4:
            line_chart()
        elif ch == 5:
            while True:
                print("Pie Charts Available: ")
                print("A. Type of Orders placed")
                print("B. Weather Condition")
                print("C. Delivery Person Age")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    pie_chart1()
                elif choice == 'B':
                    pie_chart2()
                elif choice == 'C':
                    pie_chart3()
                else:
                    print("Invalid Pie Chart option")
                    break
        elif ch == 6:
            while True:
                print("Scatter Charts Available: ")
                print("A. Orders based on Weather and Traffic")
                print("B. Average Time taken based on Weather and Traffic")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    scatter_chart1()
                elif choice == 'B':
                    scatter_chart2()
                else:
                    print("Invalid option")
                    break
        elif ch == 7:
            box()
        elif ch == 8:
            while True:
                print("Maps Available: ")
                print("A. Restaurants and Delivery Locations on Map")
                print("B. Particular Mapping of Restaurant to Delivery Locations on Map")
                print("C. One Particular Mapping of Restaurant to Delivery Locations on Map")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    geo_map()
                elif choice == 'B':
                    geo_map1()
                elif choice == 'C':
                    geo_map2()
                else:
                    print("Invalid option")
                    break
        else:
            print("Invalid Option")
            exit("Thank You!!!")
