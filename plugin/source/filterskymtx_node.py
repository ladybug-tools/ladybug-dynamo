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
        #Get path to dynamo package using the package name
        dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
        appdata = os.getenv('APPDATA')
        return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Ladybug'))

    ###### start you code from here ###
    from ladybugdynamo.wrapper import Wrapper
    from ladybugdynamo.sky import CumulativeSkyMtx

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
