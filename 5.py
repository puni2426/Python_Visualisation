import pymongo
import plotly.graph_objs as go

# establish a connection to the MongoDB server
client = pymongo.MongoClient("mongodb://localhost:27017/")

# get a handle to the database and collection
db = client["datas"]
collection = db["trail1"]

# construct the aggregation pipeline
pipeline = [
    {"$group": {"_id": "$Weatherconditions", "count": {"$sum": 1}}}
]

# execute the aggregation pipeline
results = list(collection.aggregate(pipeline))

# extract the x and y values for the bar graph
x = [r["_id"] for r in results]
y = [r["count"] for r in results]

# create the bar graph
fig = go.Figure(data=[go.Bar(x=x, y=y)])

# set the layout properties for the bar graph
fig.update_layout(
    title="Weatherconditions Distribution",
    xaxis_title="Weatherconditions",
    yaxis_title="Count"
)

# display the bar graph
fig.show()