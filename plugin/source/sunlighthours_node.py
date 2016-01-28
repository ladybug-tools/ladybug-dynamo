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
        #Get path to dynamo package using the package name
        dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
        appdata = os.getenv('APPDATA')
        return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Ladybug'))

    ###### start you code from here ###
    import ladybugdynamo.sunlighthours as sunlighthours


    # get input data
    testPoints = IN[0] if isinstance(IN[0], list) else [IN[0]]
    geometries = IN[1] if isinstance(IN[1], list) else [IN[1]]
    sunVectors = IN[2] if isinstance(IN[2], list) else [IN[2]]

    # TODO: Integrate datetime into analysis
    slh = sunlighthours.Sunlighthours(sunVectors, [], testPoints, geometries)
    slh.runAnalysis()

    # assign outputs
    OUT = copy.deepcopy(slh.results)
    del(slh)
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
