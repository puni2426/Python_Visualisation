# from pymongo import MongoClient
# from geopy.geocoders import Nominatim
#
# # Connect to MongoDB database
# client = MongoClient('mongodb://localhost:27017/')
# db = client['datas']
# collection = db['train']
#
# # Get the latitude and longitude from the collection
# document = collection.find_one()
# latitude = document['Restaurant_latitude']
# longitude = document['Restaurant_longitude']
#
# # Use geopy to get the place name
# geolocator = Nominatim(user_agent='myapp')
# location = geolocator.reverse(f"{latitude}, {longitude}")
# place_name = location.address
#
# # Print the place name
# print(place_name)
import folium
from pymongo import MongoClient

# connect to your MongoDB server
client = MongoClient('localhost', 27017)

# select your database and collection
db = client['datas']
collection = db['train1']

# retrieve the latitude and longitude values from your collection
latitude = collection.find_one()['Restaurant_latitude']
longitude = collection.find_one()['Restaurant_longitude']

# create a map centered at the given latitude and longitude
my_map = folium.Map(location=[latitude, longitude], zoom_start=10)

# add a marker at the given latitude and longitude
folium.Marker(location=[latitude, longitude]).add_to(my_map)

# display the map in a web browser
my_map.show_in_browser()
