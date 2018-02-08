# assign inputs
_location = IN[0]
name = latitude = longitude = timeZone = elevation = None

try:
    import ladybug.location as loc
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _location:
    # in case someone uses the input from an older version of ladybug
    location = loc.Location.from_location(_location)
    name = location.city
    latitude = location.latitude
    longitude = location.longitude
    timeZone = location.time_zone
    elevation = location.elevation

# assign outputs to OUT
OUT = name, latitude, longitude, timeZone, elevation