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

    # get input data
    # unwrap sky
    try:
        cSky = IN[0].unwrap()
    except:
        raise ValueError("Can't be unwrapped. Input sky is not a LBCumulativeSky")

    # instance check fails!
    #assert isinstance(cSky, CumulativeSkyMtx), "Input sky is not a LBCumulativeSky"
    assert type(cSky).__name__ == "CumulativeSkyMtx", "Input sky is not a LBCumulativeSky"

    # get hours of the year
    HOYs = IN[1] if isinstance(IN[1], list) else [IN[1]]
    includeDiffuse = IN[2]
    includeDirect = IN[3]

    cSky.gendaymtx(diffuse = includeDiffuse, direct = includeDirect, \
        analysisPeriod = HOYs)

    #Assign your output to the OUT variable.
    OUT = [Wrapper(cSky), \
    		[cSky.skyTotalRadiation.values(header = True),
            cSky.skyDiffuseRadiation.values(header = True),
            cSky.skyDirectRadiation.values(header = True)]
          ]
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
