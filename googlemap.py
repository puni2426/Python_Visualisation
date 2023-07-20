import folium
import googlemaps

# Initialize the Google Maps client
gmaps = googlemaps.Client(api_key='YOUR_API_KEY')

# Define the location coordinates
restaurant_lat, restaurant_long = 22.745049, 75.892471
delivery_lat, delivery_long = 22.765049, 75.912471

# Get the street view image URLs for the locations
restaurant_street_view = gmaps.streetview(location=(restaurant_lat, restaurant_long), size=(300, 300))
delivery_street_view = gmaps.streetview(location=(delivery_lat, delivery_long), size=(300, 300))

# Create HTML strings for the street view images
restaurant_popup = f'<img src="{restaurant_street_view.url}">'
delivery_popup = f'<img src="{delivery_street_view.url}">'

# Create the map and markers
my_map = folium.Map(location=[restaurant_lat, restaurant_long], zoom_start=14)

restaurant_marker = folium.Marker(location=[restaurant_lat, restaurant_long],
                                  tooltip="Restaurant Location",
                                  icon=folium.Icon(color='purple', icon='star'),
                                  popup=folium.Popup(restaurant_popup, max_width=300))
restaurant_marker.add_to(my_map)

delivery_marker = folium.Marker(location=[delivery_lat, delivery_long],
                                tooltip="Delivery Location",
                                icon=folium.Icon(color='red', icon='home'),
                                popup=folium.Popup(delivery_popup, max_width=300))
delivery_marker.add_to(my_map)

# Display the map
my_map.save('geoMap1.html')
my_map.show_in_browser()
