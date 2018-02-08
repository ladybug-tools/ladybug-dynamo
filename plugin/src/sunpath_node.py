# assign inputs
north_, _location, _hoys_, _centerPt_, _scale_, _sunScale_, _annual_ = IN
vectors = altitudes = azimuths = sunPts = analemma = compass = daily = centerPt = hoys = datetimes = None

try:
    from ladybug.sunpath import Sunpath
    import ladybug.geometry as geo
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _location:
    
    daylightSavingPeriod = None  # temporary until we fully implement it
    _hoys_ = _hoys_ or ()

    # initiate sunpath based on location
    sp = Sunpath.from_location(_location, north_, daylightSavingPeriod)

    # draw sunpath geometry
    sunpath_geo = \
        sp.draw_sunpath(_hoys_, _centerPt_, _scale_, _sunScale_, _annual_)
    
    analemma = sunpath_geo.analemma_curves
    compass = sunpath_geo.compass_curves
    daily = sunpath_geo.daily_curves
    
    sunPts = sunpath_geo.sun_geos

    suns = sunpath_geo.suns
    vectors = (geo.vector(*sun.sun_vector) for sun in suns)
    altitudes = (sun.altitude for sun in suns)
    azimuths = (sun.azimuth for sun in suns)
    centerPt = _centerPt_ or geo.point(0, 0, 0)
    hoys = (sun.hoy for sun in suns)
    datetimes = (sun.datetime for sun in suns)

# assign outputs to OUT
OUT = vectors, altitudes, azimuths, sunPts, analemma, compass, daily, centerPt, hoys, datetimes