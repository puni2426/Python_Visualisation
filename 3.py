import pymongo
import csv

# create a MongoClient object and connect to the running MongoDB instance
client = pymongo.MongoClient()

# select a database
db = client['datas']

# select a collection
collection = db['train1']

# open the CSV file
with open('/home/ee212821/Downloads/trail1.csv') as f:
    # create a CSV reader object
    reader = csv.DictReader(f)
    # read the data from the file into a list of dictionaries
    data = [dict(row) for row in reader]

# insert the data into the collection
result = collection.insert_many(data)

# print the object IDs of the inserted documents
print(result.inserted_ids)