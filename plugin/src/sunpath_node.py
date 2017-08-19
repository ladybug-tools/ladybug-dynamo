# assign inputs
north_, _location, _hoys_, _centerPt_, _scale_, _sunScale_, _annualSunpath_ = IN
sunVectors = sunAltitudes = sunAzimuths = sunSpheres = geometry = centerPt = sunPositions = hoys = datetimes = None


try:
    from ladybug.dt import DateTime
    from ladybug.sunpath import Sunpath
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _location:

    daylightSavingPeriod = None  # temporary until we fully implement it
    
    # initiate sunpath based on location
    sp = Sunpath.fromLocation(_location, north_, daylightSavingPeriod,
        basePoint=_centerPt_, scale=_scale_, sunScale=_sunScale_)
    
    # draw suns
    months = {}
    for HOY in _hoys_:
        dt = LBDateTime.fromHOY(HOY)
        sp.drawSunFromDateTime(dt)
    
    # draw daily sunpath curves
    # draw sunpath geometry
    sp.drawSunpath(_hoys_, annual=_annualSunpath_)
    #if not _annualSunpath_ and dt.DOY not in months:
    #    # add this day
    #    sp.drawDailySunpath(dt.month, dt.day)
    #    months[dt.DOY] = dt  # keep track of days not to redraw them

    # generate outputs
    suns = sp.suns
    sunCount = len(suns)
    sunVectors = range(sunCount)
    sunAltitudes = range(sunCount)
    sunAzimuths = range(sunCount)
    sunPositions = range(sunCount)
    sunDateTimes = range(sunCount)
    
    for count, sun in enumerate(suns):
        sunVectors[count] = sun.vector
        sunAltitudes[count] = sun.altitude
        sunAzimuths[count] = sun.azimuth
        sunPositions[count] = sun.position
        sunDateTimes[count] = sun.datetime
    
    geometries = sp.geometries.values()
    sunSpheres = sp.sunGeometries
    centerPoint = sp.basePoint


# assign outputs to OUT
OUT = sunVectors, sunAltitudes, sunAzimuths, sunSpheres, geometry, centerPt, sunPositions, hoys, datetimes