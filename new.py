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
    plt.savefig("hist.png")


def bar_graph():
    while 1:
        print("Bar Graphs Available: ")
        print("1. Traffic Density with respect to City and Delivery Rating Achieved")
        print("2. Delivery Person Rating with respect to Delivery Rating")
        print("3. Number of Orders with respect to City")
        choice = input("Enter the choice: ")
        if choice == 1:
            pass
        elif choice == 2:
            data = list(collection.find({}, {"Delivery_person_Ratings": 1, "Delivery_person_Age": 1, "_id": 0}))
            field1_values = [d["Delivery_person_Ratings"] for d in data]
            field2_values = [d["Delivery_person_Age"] for d in data]
            # plot data
            plt.bar(field1_values, field2_values, color='maroon', width=0.05)
            plt.xlabel("Delivery person ratings")
            plt.ylabel("Delivery person age")
            plt.title("Bar Chart")
            plt.legend(loc='upper right')
            plt.savefig("bar2.png")
        else:
            return 0


def pie_chart():
    # retrieve data from collection
    data = collection.find({}, {'_id': 0, 'Type_of_order': 1})
    # create lists for x and y axis data
    x_data = []
    for item in data:
        x_data.append(item['Type_of_order'])
    # create bar chart
    x = x_data.count("Snack ")
    y = x_data.count("Meal ")
    z = x_data.count("Buffet ")
    a = x_data.count("Drinks ")
    z1 = np.array([x / 1.5, y, z, a])
    x1 = ["Snack", "Meal", "Buffet", "Drinks"]
    y1=[.2,.2,.2,.2]
    plt.pie(z1, labels=x1, autopct='%.2f%%')
    plt.axis('equal')
    plt.legend(title='Type of Order')
    plt.savefig("pie_chart.png")



if __name__ == "__main__":
    print("-------------------------Welcome to Geo Coding------------------------")
    while(1):
        print("1. Push Data\n2. Histogram\n3. Bar Chart\n4. Line Chart\n5. Pie Chart\n6. Scatter Chart\n7. Geo Map")
        ch = int(input("Enter your choice: \n"))
        if ch == 1:
            push_data()
        elif ch == 2:
            histogram()
        elif ch == 3:
            bar_graph()
        # elif ch == 4:
        #     line_chart()
        elif ch == 5:
            pie_chart()
        # elif ch == 6:
        #     scatter_chart()
        # elif ch == 7:
        #     geo_map()
        else:
            exit("Thank You!!!")
