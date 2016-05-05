try:
    # add IronPython path to sys
    import sys
    IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
    sys.path.append(IronPythonLib)

    # Now that the path to IronPython is established we can import libraries
    import os
    import clr
    import copy
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
    import ladybugdynamo.solarradiation as radiation
    from ladybugdynamo.sky import CumulativeSkyMtx

    # get input data
    testPoints = IN[0] if isinstance(IN[0], list) else [IN[0]]
    pointsNormal = IN[1] if isinstance(IN[1], list) else [IN[1]]
    geometries = IN[2] if isinstance(IN[2], list) else [IN[2]]
    sky = IN[3].unwrap()

    assert type(sky).__name__ == "CumulativeSkyMtx", "Input sky is not a LBCumulativeSky"

    # TODO: Integrate datetime into analysis
    radAnalysis = radiation.SolarRadiation(sky, testPoints, pointsNormal, geometries)
    radAnalysis.runAnalysis()

    # assign outputs
    OUT = copy.deepcopy(radAnalysis.results)
    del(radAnalysis)
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
