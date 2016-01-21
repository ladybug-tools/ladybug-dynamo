# add IronPython path to sys
import sys
IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(IronPythonLib)

# Now that the path to IronPython is stablished we can import libraries
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
sunVectors = IN[0]
testPoints = IN[1]
geometries = IN[2]

# TODO: Integrate datetime into analysis
slh = sunlighthours.Sunlighthours(sunVectors, [], testPoints, geometries)
slh.runAnalysis()

# assign outputs
OUT = copy.deepcopy(slh.results)
del(slh)
