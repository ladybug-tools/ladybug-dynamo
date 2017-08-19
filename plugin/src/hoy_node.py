# assign inputs
_month_, _day_, _hour_, _minute_ = IN
hoy = doy = date = None

try:
    import ladybug.dt as dt
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

datetime = dt.DateTime(_month_, _day_, _hour_, _minute_)
hoy = datetime.hoy
doy = datetime.doy
date = datetime


# assign outputs to OUT
OUT = hoy, doy, date