try:
    # add IronPython path to sys
    import sys
    IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
    sys.path.append(IronPythonLib)

    # Now that the path to IronPython is established we can import libraries
    import os
    import clr
    clr.AddReference('DynamoCore')

    def getPackagePath(packageName):
        """Get path to dynamo package using the package name."""
        _loc = clr.References[2].Location
        _ver = _loc.split('\\')[-2].split(' ')[-1]

        # the path structure has changed after the release of version 1
        dynamoPath_1 = "Dynamo\\Dynamo Revit\\" + _ver
        dynamoPath_0 = "Dynamo\\" + _ver
        appdata = os.getenv('APPDATA')
        path1 = '%s\%s\packages\%s\extra\\' % (appdata, dynamoPath_1, packageName)
        path0 = '%s\%s\packages\%s\extra\\' % (appdata, dynamoPath_0, packageName)

        if os.path.isdir(path1):
            return path1
        elif os.path.isdir(path0):
            return path0
        else:
            raise Exception("Can't find Dynamo installation Folder!")

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Ladybug'))

    ###### start you code from here ###
    import ladybugdynamo.core as core
    import ladybugdynamo.epw as epw
    import ladybugdynamo.sunpath as sunpath

    ## calculate sunpath data
    # get location data
    northAngle = IN[0]
    location = IN[1]
    HOYs = IN[2] if isinstance(IN[2], list) else [IN[2]]
    cenPt, scale, sunScale = IN[3:6]
    drawAnnualSunpath = IN[6] # a boolean that indicates if sunpath should be drawn for

    #daylightSavingPeriod = IN[7]
    daylightSavingPeriod = None # temporary until I fully implement it

    # initiate sunpath based on location
    sp = sunpath.Sunpath.fromLocation(location, northAngle, daylightSavingPeriod, \
            basePoint =cenPt, scale = scale, sunScale = sunScale)

    # draw sunpath geometry
    if drawAnnualSunpath: sp.drawAnnualSunpath()

    # draw suns
    months = {}
    for HOY in HOYs:
        dt = core.LBDateTime.fromHOY(HOY)
        sp.drawSunFromDateTime(dt)

        #draw daily sunpath curves
        if not drawAnnualSunpath and dt.DOY not in months:
            # add this day
            sp.drawDailySunpath(dt.month, dt.day)
            months[dt.DOY] = dt  #keep track of days not to redraw them


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

    # assign outputs
    OUT = [
            sunVectors,
            sunAltitudes,
            sunAzimuths,
            sunSpheres,
            geometries,
            centerPoint,
            sunPositions,
            sunDateTimes
        ]
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
