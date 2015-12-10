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

## calculate sunpath data
# get location data
northAngle = IN[0]
location = IN[1]
HOYs = IN[2]
cenPt, scale, sunScale = IN[3:6]
drawAnnualSunpath = IN[6] # a boolean that indicates if sunpath should be drawn for
#daylightSavingPeriod = IN[7]

# initiate sunpath based on location
sp = sunpath.Sunpath.fromLocation(location, northAngle)

dynamoSp = dssunpath.DSSunpath(sp, basePoint =cenPt, scale = scale, sunScale = sunScale)

# draw sunpath geometry
if drawAnnualSunpath: dynamoSp.drawAnnualSunpath()

# draw suns
months = {}
for HOY in HOYs:
    dt = core.LBDateTime.fromHOY(HOY)
    dynamoSp.drawSunFromDateTime(dt)

    #draw daily sunpath curves
    if not drawAnnualSunpath and dt.DOY not in months:
        # add this day
        dynamoSp.drawDailySunpath(dt.month, dt.day)
        months[dt.DOY] = dt  #keep track of days not to redraw them


# generate outputs
suns = dynamoSp.suns
sunCount = len(suns)
sunVectors = range(sunCount)
sunAltitudes = range(sunCount)
sunAzimuths = range(sunCount)
sunPositions = range(sunCount)
sunDateTimes = range(sunCount)

for count, sun in enumerate(suns):
    sunVectors[count] = sun.vector
    sunAltitudes[count] = sun.altitude
    sunAzimuths[count] = sun.azimuth
    sunPositions[count] = sun.position
    sunDateTimes[count] = sun.datetime

geometries = dynamoSp.dailyCurves + \
            dynamoSp.analemmaCurves + \
            dynamoSp.baseCurves

sunSpheres = dynamoSp.sunGeometries
centerPoint = dynamoSp.basePoint

# assign outputs
OUT = [
        sunVectors,
        sunAltitudes,
        sunAzimuths,
        sunSpheres,
        geometries,
        centerPoint,
        sunPositions,
        sunDateTimes
    ]
