try:
    # add IronPython path to sys
    import sys
    IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
    sys.path.append(IronPythonLib)

    # Now that the path to IronPython is established we can import libraries
    # I don't need them in this case but just for testing memory
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
    from ladybugdynamo.wrapper import Wrapper
    import ladybugdynamo.sky as sky

    # get input data
    epwfile = IN[0]
    skyDensity = IN[1]
    workingDir = IN[2] if IN[2].strip()!="" else os.path.join(getPackagePath('Ladybug') + "temp\\cumulativeSkies")

    cSky = sky.CumulativeSkyMtx(epwfile, skyDensity=skyDensity, workingDir=workingDir)

    cSky.gendaymtx(pathToRadianceBinaries=getPackagePath('Ladybug').replace("extra", "bin"))
    # assign sky to output
    OUT = Wrapper(cSky)
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
