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
        #Get path to dynamo package using the package name
        dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
        appdata = os.getenv('APPDATA')
        return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Ladybug'))

    ###### start you code from here ###
    import ladybugdynamo.core as core

    ## calculate sunpath data
    # get location data
    dt = core.LBDateTime(*IN)

    OUT = [
            dt.floatHOY,
            dt.DOY,
            dt
        ]
except Exception, e:
	OUT = "ERROR: %s"%str(e) + \
		"\nIf you think this is a bug submit an issue on github.\n" + \
		"https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
