###### start you code from here ###
from ladybugdynamo.dt import LBDateTime
from ladybugdynamo.sunpath import Sunpath

# calculate sunpath data
# get location data
northAngle = IN[0]
location = IN[1]
HOYs = IN[2] if isinstance(IN[2], list) else [IN[2]]
cenPt, scale, sunScale = IN[3:6]
drawAnnualSunpath = IN[6]  # a boolean that indicates if sunpath should be drawn for

# daylightSavingPeriod = IN[7]
daylightSavingPeriod = None  # temporary until I fully implement it

# initiate sunpath based on location
sp = Sunpath.fromLocation(location, northAngle, daylightSavingPeriod,
						  basePoint=cenPt, scale=scale, sunScale=sunScale)

# draw sunpath geometry
if drawAnnualSunpath:
	sp.drawAnnualSunpath()

# draw suns
months = {}
for HOY in HOYs:
	dt = LBDateTime.fromHOY(HOY)
	sp.drawSunFromDateTime(dt)

	# draw daily sunpath curves
	if not drawAnnualSunpath and dt.DOY not in months:
		# add this day
		sp.drawDailySunpath(dt.month, dt.day)
		months[dt.DOY] = dt  # keep track of days not to redraw them

# generate outputs
suns = sp.suns
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

geometries = sp.geometries.values()
sunSpheres = sp.sunGeometries
centerPoint = sp.basePoint

# assign outputs
OUT = (
	sunVectors,
	sunAltitudes,
	sunAzimuths,
	sunSpheres,
	geometries,
	centerPoint,
	sunPositions,
	sunDateTimes
)


