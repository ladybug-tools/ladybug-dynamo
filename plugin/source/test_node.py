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
import ladybugdynamo.epw as epw
import ladybugdynamo.core as core
import ladybugdynamo.sunpath as sunpath

# This example shows how to calculate sunpath with Ladybug and draw it in Dynamo

## calculate sunpath data
# get location data
epwFile = r"C:\EnergyPlusV8-3-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw"
#epwFile = r"C:\ladybug\AUS_NSW\AUS_NSW.Cobar.947110_RMY.epw"
locationData = epw.EPW(epwFile).location
HOYs = range(9,12)
# initiate sunpath based on location
sp = sunpath.Sunpath.fromLocation(locationData, northAngle = 0)
for HOY in HOYs: sp.drawSunFromDateTime(core.LBDateTime.fromHOY(HOY))
suns = sp.suns
