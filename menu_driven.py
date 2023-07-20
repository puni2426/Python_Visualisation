import pymongo
import csv
import matplotlib.pyplot as plt
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


def histogram():
    result = collection.aggregate([{"$group": {"_id": "$Delivery_person_Ratings", "count": {"$sum": 1}}}])
    x_axis = []
    y_axis = []
    for doc in result:
        x_axis.append(float(doc["_id"]))
        y_axis.append(float(doc["count"]))
    plt.bar(x_axis, y_axis)
    plt.xlabel("Delivery Person Rating")
    plt.ylabel("Order Count")
    plt.title("Orders by Delivery Person Rating")
    plt.show()


def bar_graph():
    result = collection.aggregate([{"$group": {"_id": "$City", "count": {"$sum": 1}}}])

    x_axis = []
    y_axis = []

    for doc in result:
        x_axis.append(doc["_id"])
        y_axis.append(doc["count"])

    plt.bar(x_axis, y_axis)
    plt.xlabel("City")
    plt.ylabel("Count")
    plt.title("Orders by City")
    plt.show()


def line_chart():
    result = collection.aggregate([{"$group": {"_id": "$Order_Date", "count": {"$sum": 1}}}, {"$sort": {"_id": 1}}])

    x_axis = []
    y_axis = []

    for doc in result:
        x_axis.append(doc["_id"])
        y_axis.append(doc["count"])

    plt.plot(x_axis, y_axis)
    plt.xlabel("Date")
    plt.ylabel("Count")
    plt.title("Orders by Date")
    plt.show()


def pie_chart():
    # retrieve data from collection
    result = collection.aggregate([{"$group": {"_id": "$Type_of_order", "count": {"$sum": 1}}}])

    labels = []
    sizes = []

    for doc in result:
        labels.append(doc["_id"])
        sizes.append(doc["count"])

    plt.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
    plt.title("Orders by Type")
    plt.axis("equal")
    plt.legend()
    plt.show()


def scatter_chart():
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
    plt.show()


if __name__ == "__main__":
    print("-------------------------Welcome to Geo Coding------------------------")
    while 1:
        print("1. Push Data\n2. Histogram\n3. Bar Chart\n4. Line Chart\n5. Pie Chart\n6. Scatter Chart\n7. Geo Map")
        ch = int(input("Enter your choice: \n"))
        if ch == 1:
            push_data()
        elif ch == 2:
            histogram()
        elif ch == 3:
            bar_graph()
        elif ch == 4:
            line_chart()
        elif ch == 5:
            pie_chart()
        elif ch == 6:
            scatter_chart()
        # elif ch == 7:
        #     geo_map()
        else:
            exit("Thank You!!!")