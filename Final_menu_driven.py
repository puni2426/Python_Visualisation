import pymongo
import csv
import matplotlib.pyplot as plt
import pandas as pd
import folium
import numpy as np

# create a MongoClient object and connect to the running MongoDB instance
client = pymongo.MongoClient()
# select a database
db = client['datas']
# select a collection
collection = db['trail1']


# open the CSV file
def push_data():
    with open('/home/ee212821/Downloads/Dataset1.csv') as f:
        # create a CSV reader object
        reader = csv.DictReader(f)
        # read the data from the file into a list of dictionaries
        data = [dict(row) for row in reader]
    # insert the data into the collection
    result = collection.insert_many(data)


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
    plt.hist(values, weights=counts, bins=20)
    plt.xlabel("Time Taken")
    plt.ylabel("Count")
    plt.title("Delivery Time Histogram")
    plt.show()


def histogram2():
    pipeline = [
        {"$group": {"_id": None, "Delivery_person_Age": {"$push": "$Delivery_person_Age"}}}
    ]
    results = collection.aggregate(pipeline)
    x_axis=[]
    for i in results:
        x_axis.append(i['Delivery_person_Age'])
    # Create and display the histogram graph
    plt.hist(x_axis, color="#B4F8C8")
    plt.title('Histogram of Delivery person Age')
    plt.xlabel('Delivery person_Age')
    plt.ylabel('Frequency')
    plt.show()

def bar_graph1():
    data = list(collection.find({}, {'City': 1, 'Road_traffic_density': 1, "Delivery_person_Ratings": 1, "_id": 0}))
    index_values = [d['City'] for d in data]
    columns_values = [d['Road_traffic_density'] for d in data]
    df = pd.read_csv('/home/ee212821/Downloads/Dataset1.csv')
    df = df.groupby(['City', 'Road_traffic_density'])['Delivery_person_Ratings'].mean().reset_index()
    df.pivot(index='City', columns='Road_traffic_density', values='Delivery_person_Ratings').plot(kind='bar')
    plt.xlabel('City')
    plt.ylabel('Delivery person Ratings')
    plt.title('Traffic Density with respect to City and Delivery Rating Achieved')
    plt.legend(loc='upper right')
    plt.savefig('Bar1.png')
    plt.show()


def bar_graph2():
    data = list(collection.find({}, {"Delivery_person_Ratings": 1, "Delivery_person_Age": 1, "_id": 0}))
    field1_values = sorted([d["Delivery_person_Age"] for d in data])
    field2_values = [d["Delivery_person_Ratings"] for d in data]
    # plot data
    plt.bar(field1_values, field2_values, color='maroon', width=.8)
    plt.xlabel("Delivery person age")
    plt.ylabel("Delivery person ratings")
    plt.title("Bar Chart")
    plt.savefig('Bar2.png')
    plt.show()


def bar_graph3():
    result = collection.aggregate([{"$group": {"_id": "$Road_traffic_density", "count": {"$sum": 1}}},{"$sort":{"count":-1}}])
    x_axis = []
    y_axis = []
    for doc in result:
        x_axis.append(doc["_id"])
        y_axis.append(doc["count"])
    plt.bar(x_axis, y_axis, color ="g")
    plt.xlabel("Road traffic density")
    plt.ylabel("Count")
    plt.title("Orders by Road traffic density")
    plt.savefig('Bar3.png')
    plt.show()


def line_chart():
    result = collection.aggregate([{"$group": {"_id": "$Time_taken", "count": {"$sum": 1}}}, {"$sort": {"_id": 1}}])
    x_axis = []
    y_axis = []
    for doc in result:
        x_axis.append(doc["_id"])
        y_axis.append(doc["count"])
    # plt.plot(x_axis, y_axis)
    # plot the data with a red line, blue markers, and green fill
    plt.plot(x_axis, y_axis, color='red', marker='o', markerfacecolor='blue', fillstyle='full', alpha=0.5)

    plt.xlabel("Time Taken")
    plt.ylabel("Count")
    plt.title("Order by Time taken")
    plt.savefig('line1.png')
    plt.show()


def pie_chart1():
    # retrieve data from collection
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


def pie_chart2():
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


def pie_chart3():
    result = collection.aggregate([{"$group": {"_id": "$Delivery_person_Age", "count": {"$sum": 1}}}])
    labels = []
    sizes = []
    for doc in result:
        labels.append(doc["_id"])
        sizes.append(doc["count"])
    plt.pie(sizes, labels=labels, autopct="%.1f%%", startangle=90)
    plt.title("Delivery_person_Age")
    plt.axis("equal")
    plt.savefig('Pie3.png')
    plt.show()


def scatter_chart1():
    result = collection.aggregate([{"$group": {
        "_id": {"weather": "$Weatherconditions", "traffic": "$Road_traffic_density"}, "count": {"$sum": 1}}}])
    x_axis = []
    y_axis = []
    sizes = []
    for doc in result:
        x_axis.append(doc["_id"]["weather"])
        y_axis.append(doc["_id"]["traffic"])
        sizes.append(doc["count"])

    plt.scatter(x_axis, y_axis, s=sizes)
    plt.xlabel("Weather Conditions")
    plt.ylabel("Road Traffic Density")
    plt.title("Orders by Weather and Traffic")
    plt.savefig('scatter1.png')
    plt.show()


def scatter_chart2():
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
        ranks.append(i + 1)
    colors = np.random.rand(25)
    # Create a scatter plot with rank
    plt.scatter(ranks, y_values, c=colors)
    plt.xlabel("Rank")
    plt.ylabel("Average Time Taken")
    plt.title("Delivery Time vs Traffic Density with Rank")
    # Display the plot
    plt.savefig('scatter1.png')
    plt.show()

def box_graph():
    pipeline = [{"$group": {"_id": "$Type_of_vehicle", "Time_taken": {"$push": "$Time_taken"}}}]
    result = list(db.trail1.aggregate(pipeline))
    data = [r["Time_taken"] for r in result]
    labels = [r["_id"] for r in result]
    plt.boxplot(data, labels=labels)
    plt.title("Delivery Time by Vehicle Type")
    plt.xlabel("Vehicle Type")
    plt.ylabel("Time Taken (min)")
    plt.savefig('box_graph.png')
    plt.show()


def geo_map():
    data = []
    for doc in collection.find():
        latitudeR = doc['Restaurant_latitude']
        longitudeR = doc['Restaurant_longitude']
        latitudeD = doc['Delivery_location_latitude']
        longitudeD = doc['Delivery_location_longitude']
        data.append((latitudeR, longitudeR, latitudeD, longitudeD))
    my_map = folium.Map(location=[doc['Restaurant_latitude'], doc['Restaurant_longitude']], zoom_start=10)
    for latitudeR, longitudeR, latitudeD, longitudeD in data:
        Restaurant_popup = ('<strong>Restaurant latitude</strong>: ' + str(
            doc['Restaurant_latitude']) + '<br>''<strong>Restaurant longitude</strong>: ' + str(
            doc['Restaurant_longitude']) + '<br>')
        restaurant_marker = folium.Marker(location=[latitudeR, longitudeR], tooltip="Restaurant Location",
                                          icon=folium.Icon(color='purple', icon='star'), popup=Restaurant_popup)
        restaurant_marker.add_to(my_map)
        Delivery_popup = ('<strong>Delivery latitude</strong>: ' + str(
            doc['Delivery_location_latitude']) + '<br>''<strong>Delivery longitude</strong>: ' + str(
            doc['Delivery_location_longitude']) + '<br>'
                                                  '<strong>Delivery Rating</strong>: ' + str(
            doc['Delivery_person_Ratings']) + '<br>')
        delivery_marker = folium.Marker(location=[latitudeD, longitudeD], tooltip="Delivery Location",
                                        icon=folium.Icon(color='red', icon='home'), popup=Delivery_popup)
        delivery_marker.add_to(my_map)
    # Display the map
    my_map.save('geoMap.html')
    my_map.show_in_browser()


def geo_map1():
    my_map = folium.Map(location=[22.745049, 75.892471], zoom_start=10)
    Restaurant_popup = ('<strong>Restaurant latitude :</strong>' + str(
        '22.745049') + '<br>''<strong>Restaurant longitude :</strong>' + str('75.892471') + '<br>')
    restaurant_marker = folium.Marker(location=[22.745049, 75.892471], tooltip="Restaurant Location",
                                      icon=folium.Icon(color='purple', icon='star'), popup=Restaurant_popup)
    restaurant_marker.add_to(my_map)
    Delivery_popup = ('<strong>Delivery latitude :</strong>' + str(
        '22.765049') + '<br>''<strong>Delivery longitude :</strong>' + str('75.912471') + '<br>'
                                                                                          '<strong>Delivery Rating - </strong>' + str(
        '4.9') + '<br>')
    delivery_marker = folium.Marker(location=[22.765049, 75.912471], tooltip="Delivery Location",
                                    icon=folium.Icon(color='red', icon='home'), popup=Delivery_popup)
    delivery_marker.add_to(my_map)
    folium.PolyLine(locations=[[22.745049, 75.892471], [22.765049, 75.912471]], clinewidth=1, color='#69b3a2').add_to(
        my_map)
    # Display the map
    my_map.save('geoMap1.html')
    my_map.show_in_browser()


if __name__ == '__main__':
    print("-------------------------Welcome to Geo Coding------------------------")
    while True:
        print("1. Push Data\n2. Histogram\n3. Bar Chart\n4. Line Chart\n5. Pie Chart\n6. Scatter Chart\n7. Box Graph\n8. Geo Map")
        ch = int(input("Enter your choice: \n"))
        if ch == 1:
            push_data()
        elif ch == 2:
            while True:
                print("Histogram Available: ")
                print("A. Orders by Delivery Person Rating")
                print("B. Delivery Person Rating with respect to Delivery Rating")
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
                print("B. Delivery Person Rating with respect to Delivery Rating")
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
                print("A. Restaurants and Delivery Locations on Map")
                print("B. One Particular Mapping of Restaurant to Delivery Locations on Map")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    scatter_chart1()
                elif choice == 'B':
                    scatter_chart2()
                else:
                    print("Invalid option")
                    break
        elif ch == 7:
            box_graph()
        elif ch == 8:
            while True:
                print("Maps Available: ")
                print("A. Restaurants and Delivery Locations on Map")
                print("B. One Particular Mapping of Restaurant to Delivery Locations on Map")
                choice = input("Enter the choice: ")
                if choice == 'A':
                    geo_map()
                elif choice == 'B':
                    geo_map1()
                else:
                    print("Invalid option")
                    break
        else:
            exit("Thank You!!!")