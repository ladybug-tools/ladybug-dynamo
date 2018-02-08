# assign inputs
_name_, _latitude_, _longitude_, _timeZone_, _elevation_ = IN
location = None

try:
    import ladybug.location as loc
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

location = loc.Location(_name_, '-', _latitude_, _longitude_, _timeZone_, _elevation_)

# assign outputs to OUT
OUT = (location,)