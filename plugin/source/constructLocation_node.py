###### start you code from here ###

# import Ladybug libraries
from ladybugdynamo.location import Location

# read Dynamo inputs
city, latitude, longitude, timeZone, elevation = IN

# create a ladybug location
location = Location()
location.city = city
location.latitude = latitude
location.longitude = longitude
location.timezone = timeZone
location.elevation = elevation

OUT = location