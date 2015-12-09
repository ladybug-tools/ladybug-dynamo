# add IronPython path to sys
import sys
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
import ladybug.core as core
import ladybug.epw as epw
import ladybug.sunpath as sunpath
import ladybugdynamo.dynamosunpath as dssunpath

# This example shows how to calculate sunpath with Ladybug and draw it in Dynamo

## calculate sunpath data
# get location data
epwFile = r"C:\EnergyPlusV8-3-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
locationData = epw.EPW(epwFile).location

# initiate sunpath based on location
sp = sunpath.Sunpath.fromLocation(locationData, northAngle = 0)
dynamoSp = dssunpath.DSSunpath(sp)
dynamoSp.drawAnnualSunpath()
OUT = dynamoSp.geometries.values()
