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
    sp = Sunpath.fromLocation(_location, north_, daylightSavingPeriod)

    # draw sunpath geometry
    sunpathGeo = \
        sp.drawSunpath(_hoys_, _centerPt_, _scale_, _sunScale_, _annual_)
    
    analemma = sunpathGeo.analemmaCurves
    compass = sunpathGeo.compassCurves
    daily = sunpathGeo.dailyCurves
    
    sunPts = sunpathGeo.sunGeos

    suns = sunpathGeo.suns
    vectors = (geo.vector(*sun.sunVector) for sun in suns)
    altitudes = (sun.altitude for sun in suns)
    azimuths = (sun.azimuth for sun in suns)
    centerPt = _centerPt_ or geo.point(0, 0, 0)
    hoys = (sun.hoy for sun in suns)
    datetimes = (sun.datetime for sun in suns)

# assign outputs to OUT
OUT = vectors, altitudes, azimuths, sunPts, analemma, compass, daily, centerPt, hoys, datetimes