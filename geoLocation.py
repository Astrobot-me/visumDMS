import geocoder
from geopy.geocoders import Nominatim

# Get approximate location using IP
g = geocoder.ip('me')

# Extract latitude and longitude
latitude, longitude = g.latlng

print(f"Latitude: {latitude}, Longitude: {longitude}")

# Use geopy for reverse geocoding
geolocator = Nominatim(user_agent="myappforlocation")
location = geolocator.reverse((float(latitude), float(longitude)))

print(f"Address: {location}")
