# add IronPython path to sys
import sys
import copy
IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(IronPythonLib)

# Now that the path to IronPython is stablished we can import libraries
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
import ladybugdynamo.sky as sky


# get input data
epwfile = IN[0]
skyDensity = IN[1]
workingDir = IN[2]

cSky = sky.CumulativeSkyMtx(epwfile,  skyDensity= skyDensity, workingDir = workingDir)
cSky.gendaymtx()

# assign outputs
OUT = cSky
