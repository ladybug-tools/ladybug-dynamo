# assign inputs
_epwFile = IN[0]
location = None

try:
    import ladybug.epw as epw
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _epwFile:
    ep = epw.EPW(_epwFile)
    location = ep.location

# assign outputs to OUT
OUT = (location,)