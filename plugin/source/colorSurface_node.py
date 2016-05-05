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

    def getDynamoPath():
        return os.path.split(clr.References[2].Location)[0]

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Ladybug'))
    sys.path.append(getDynamoPath())  # This is for using colors

    ###### start you code from here ###
    import ladybugdynamo.legendparameters as legendpar
    from ladybugdynamo.wrapper import Wrapper


    # analysis surfaces will be useful for drawing the legend. No use for now.
    analysisSurfaces = IN[0]
    values = IN[1]

    # I couldn't figure out why isinstance(IN[2], Wrapper) returns Flase
    # Thta's why I'm using try/exception
    #legendPar = IN[2].unwrap() if isinstance(IN[2], Wrapper) else legendpar.LegendParameters()

    try:
        legendPar = IN[2].unwrap()
    except:
        legendPar = legendpar.LegendParameters()


    OUT = legendPar.calculateColors(values)
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
