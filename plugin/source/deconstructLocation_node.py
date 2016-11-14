# import Ladybug libraries
from ladybugdynamo.location import Location

# create a ladybug location
location = Location.fromLocation(IN[0])

OUT = (
	location.city,
	location.latitude,
	location.longitude,
	location.timezone,
	location.elevation
)