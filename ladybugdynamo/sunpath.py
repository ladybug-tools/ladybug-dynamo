from ladybug.sunpath import *

# import Dynamo libraries
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

class Sunpath(LBSunpath):
    """
    Calculates sun path for Dynamo

    Attributes:
        latitude: The latitude of the location. Values must be between -90 and 90. Default is set to the equator.
        northAngle: Angle to north (0-360). 90 is west and 270 is east (Default: 0)
        longitude: The longitude of the location (Default: 0)
        timeZone: A number representing the time zone of the location you are constructing. This can improve the accuracy of the resulting sun plot.  The time zone should follow the epw convention and should be between -12 and +12, where 0 is at Greenwich, UK, positive values are to the East of Greenwich and negative values are to the West.
        daylightSavingPeriod: An analysis period for daylight saving. (Default = None)
        basePoint: A DS point that will be used as the center of sunpath. Default is Origin
        scale: A number larger than 0 for scale of sunpath
        sunScale: A number larger than 0 for scale of sun spheres

    Usage:
        import ladybugdynamo.epw as epw
        import ladybugdynamo.sunpath as sunpath

        # initiate sunpath based on location
        epwWeatherFile = r"c:\yourEpwFile.epw"
        location = epw.EPW(epwWeatherFile).location
        sp = sunpath.Sunpath.fromLocation(location)
        hourlyCurves = sp.draw()
    """

    def __init__(self, latitude = 0, northAngle = 0, longitude = 0, timeZone = 0,
                daylightSavingPeriod = None, basePoint = None, scale = 1, sunScale = 1):

        # NOTE
        # The use of self.__class__ instead of name of subclass can be tricky in case of creating
        # a new subclass from sunpath unless it provides it's own init but it was the only way that I could
        # get it to work for now.
        # Read more here: http://stackoverflow.com/questions/576169/understanding-python-super-with-init-methods
        super(self.__class__, self).__init__(latitude, northAngle, longitude, timeZone, daylightSavingPeriod)

        if not basePoint: basePoint = Point.Origin()
        self.basePoint = Point.ByCoordinates(basePoint.X, basePoint.Y, basePoint.Z)

        self.scale = float(scale) #scale of the whole sunpath
        self.sunScale = float(sunScale) * self.scale #scale for sun s
        self.__radius = 50
        self.__suns = [] # placeholder for sun(s)
        self.__dailyCurves = []
        self.__analemmaCurves = []
        self.__baseCurves = []

    @classmethod
    def fromLocation(cls, location, northAngle = 0, daylightSavingPeriod = None, \
            basePoint = None, scale = 1, sunScale = 1):
        """Create sunpath from location data"""
        sp = super(Sunpath, cls).fromLocation(location, northAngle, daylightSavingPeriod)

        if not basePoint: basePoint = Point.Origin()
        sp.basePoint = Point.ByCoordinates(basePoint.X, basePoint.Y, basePoint.Z)

        sp.scale = float(scale) #scale of the whole sunpath
        sp.sunScale = float(sunScale) * sp.scale #scale for sun s
        return sp

    @property
    def geometries(self):
        return {
        'dailyCurves': self.__dailyCurves,
        'analemmaCurves': self.__analemmaCurves,
        'baseCurves': self.__baseCurves,
        'suns': self.sunGeometries
        }

    @property
    def suns(self):
        """Get list of suns"""
        return self.__suns

    @property
    def sunGeometries(self):
        """Get list of suns"""
        if not len(self.__suns): return self.__suns #emapty list
        return [sun.geometry for sun in self.__suns]

    def removeSuns(self):
        self.__suns = []
        return True

        """Remove all suns from the sunpath"""

    @property
    def dailyCurves(self):
        """Get daily curves as a list"""
        return self.__dailyCurves

    @property
    def analemmaCurves(self):
        """Get daily curves as a list"""
        return self.__analemmaCurves

    @property
    def baseCurves(self):
        """Get daily curves as a list"""
        return self.__baseCurves

    def drawSun(self, month, day, hour, isSolarTime = False):
        """Draw a sun based on month, day and hour"""
        #create a dateTime to check the input
        sun = self.calculateSunPosition(month, day, hour, isSolarTime)

        if sun.isDuringDay: self.__suns.append(sun)

    def drawSunFromDateTime(self, dateTime, isSolarTime = False):
        """Draw a sun based on datetime"""
        self.drawSun(dateTime.month, dateTime.day, dateTime.floatHour, isSolarTime)

    def drawDailySunpath(self, month, day = 21):
        # draw curve for the day
        self.calculateDailyCurve(month, day)
        # draw baseline circles
        self.calculateBaseCurves()

    def drawAnnualSunpath(self):
        # draw analemma curves
        self.calculateAnalemmaCurves()

        # draw hourly curves
        self.calculateDailyCurves()

        # draw baseline circles
        self.calculateBaseCurves()

    def calculateSunPositionFromDateTime(self, dateTime, isSolarTime = False):
        """ Calculate the position of sun based on origin and scale

            Returns:
                sun: Returns a sun object
        """
        return self.calculateSunPosition(dateTime.month, dateTime.day, dateTime.floatHour, isSolarTime)

    def calculateSunPosition(self, month = 12, day = 21, hour = 12, isSolarTime = False):
        """ Calculate the position of sun based on origin and scale

            Returns:
                sun: A Ladybug sun object
        """
        # calculate ladybug sun for this time
        lbSun = self.calculateSun(month, day, hour, isSolarTime)

        # create a dynamo sun from ladybug sun
        sun = Sun.fromLBSun(lbSun, self.basePoint, self.__radius, self.scale, self.sunScale)

        return sun

    def calculateDailyCurve(self, month, day = 21, isSolarTime = False):
        """Calculate daily curve the day
            After calculating the curves check 'dailyCurves' property for curve geometries
        """
        # calculate sunrise, noon and sunset
        datetimesDictionary = self.calculateSunriseSunset(month, day = day, depression = 0, isSolarTime = isSolarTime)

        datetimes = [
                    datetimesDictionary['sunrise'], \
                    datetimesDictionary['noon'], \
                    datetimesDictionary['sunset']
                    ]

        dailySunPositions = []
        for datetime in datetimes:
            sun = self.calculateSunPositionFromDateTime(datetime, isSolarTime = False)
            dailySunPositions.append(sun.position)

        dailyCurve = Arc.ByThreePoints(*dailySunPositions)
        self.__dailyCurves.append(dailyCurve)

    def calculateDailyCurves(self):
        """Calculate daily curves for an annual sunpath
            After calculating the curves check 'dailyCurves' property for curve geometries
        """
        # calculate curves for 21st of all the months
        for month in range(1,13):
            self.calculateDailyCurve(month)

    def calculateAnalemmaCurves(self):
        """Calculate analemma curves for an annual sunpath
            After calculating the curves check 'dailyCurves' property for curve geometries
        """
        day = 21
        # point and plane for triming the curves
        pt = Point.ByCoordinates(0, 0, -10 + self.basePoint.Z)
        plane = Plane.ByOriginNormal(self.basePoint, Vector.ZAxis())

        for hour in range(1, 25):
            anySunUpHour = False
            anySunDownHour = False
            monthlySunPositions = []
            for month in range(1,13):
                sun = self.calculateSunPosition(month, day, hour = hour)
                if sun.isDuringDay:
                    anySunUpHour = True
                else:
                    anySunDownHour = True

                monthlySunPositions.append(sun.position)

            # all night hour
            if not anySunUpHour: continue
            # create the curve
            analemmaCurve = NurbsCurve.ByPoints(monthlySunPositions, True)

            if anySunDownHour + anySunUpHour == 2:
                # some of the hours are up hours and some are down
                # trim the curve
                curves = Geometry.Trim(analemmaCurve, plane, pt)
                # Dynamo trim doesn't work as expected
                # or I don't know how it is supposed to work so I check the curves
                selectedCurves = []
                for curve in curves:
                    # find mid point
                    midPar = (curve.EndParameter() + curve.StartParameter())/2
                    midPt = curve.PointAtParameter(midPar)
                    if midPt.Z >= self.basePoint.Z:
                        selectedCurves.append(curve)

                if len(selectedCurves)==1:
                    analemmaCurve = selectedCurves[0]
                else:
                    try:
                        # join curves
                        analemmaCurve = selectedCurves[0].Join(selectedCurves[1:])
                    except StandardError:
                        analemmaCurve = selectedCurves

            self.__analemmaCurves.append(analemmaCurve)

    def calculateBaseCurves(self):
        """Calculate base circles for sunpath"""
        self.__drawBaseCircles()
        self.__drawDirectionLines()

    # TODO: Add north angle
    def __drawDirectionLines(self):
        """Draw direction lines"""
        # create North Arrow
        startVector = Vector.Scale(Vector.YAxis(), self.scale * self.__radius)
        startPt = Point.Add(self.basePoint, startVector)
        endVector = Vector.Scale(Vector.YAxis(), 1.12 * self.scale * self.__radius)
        endPt = Point.Add(self.basePoint, endVector)
        northArrow = Line.ByStartPointEndPoint(startPt, endPt)
        # draw it for the 4 direction
        for angle in range(0, 360, 90):
            self.__baseCurves.append(northArrow.Rotate(Plane.XY(), angle + self.northAngle))

        # create mid curves
        endVector = Vector.Scale(Vector.YAxis(), 1.08 * self.scale * self.__radius)
        endPt = Point.Add(self.basePoint, endVector)
        shortArrow = Line.ByStartPointEndPoint(startPt, endPt)
        # draw it for the 4 direction
        for angle in range(0, 360, 30):
            if angle%90!=0:
                self.__baseCurves.append(shortArrow.Rotate(Plane.XY(), angle + self.northAngle))

    def __drawBaseCircles(self):
        """draw base circles"""
        innerCircle = Circle.ByCenterPointRadius(self.basePoint, self.scale * self.__radius)
        outerCircle = Circle.ByCenterPointRadius(self.basePoint, 1.02 * self.scale * self.__radius)
        outerCircle2 = Circle.ByCenterPointRadius(self.basePoint, 1.08 * self.scale * self.__radius)
        self.__baseCurves.extend([outerCircle, innerCircle, outerCircle2])


class Sun(LBSun):
    """Convert a ladybug sun to a ladybug dynamo sun

    Attributes:
        datetime: A Ladybug datetime that represents the datetime for this sunVector
        altitude: Solar Altitude in radians
        azimuth: Solar Azimuth in radians
        isSolarTime: A Boolean that indicates if datetime represents the solar time
        isDaylightSaving: A Boolean that indicates if datetime is calculated for Daylight saving period
        northAngle: North angle of the sunpath in Degrees. This will be only used to calculate the solar vector.
    """
    def __init__(self, datetime, altitude, azimuth, isSolarTime, isDaylightSaving, northAngle,
                sunpathBasePoint, sunpathScale, sunpathRadius, sunScale):

        #LBSun.__init__(datetime, altitude, azimuth, isSolarTime, isDaylightSaving, northAngle)
        super(self.__class__, self).__init__(datetime, altitude, azimuth, isSolarTime, isDaylightSaving, northAngle)
        self.__sunpathBasePoint = sunpathBasePoint
        self.__sunpathScale = sunpathScale
        self.__sunpathRadius = sunpathRadius
        self.__sunRadius = 1
        self.scale = sunScale

        # calculate vector, position and geometry
        self.__calculateGeometricalSun()

        self.__hourlyData = [] # Place holder for hourly data I'm not sure how it will work yet

    # NOTE: I assume there should be cleaner solution to do this but I couldn't figure it out
    # Ladybug sun is called under the hood in ladybug.sunpath that's
    @classmethod
    def fromLBSun(cls, LBSun, basePoint, scale, radius, sunScale):
        return cls(LBSun.datetime, LBSun.altitudeInRadians, LBSun.azimuthInRadians, LBSun.isSolarTime, \
            LBSun.isDaylightSaving, LBSun.northAngle, basePoint, scale, radius, sunScale)

    def __calculateGeometricalSun(self):
        """calculate sun vector, base point and sphere"""
        # convert sun vector to Dynamo Vector
        self.__vector = Vector.ByCoordinates(self.sunVector.x, self.sunVector.y, self.sunVector.z)

        movingVector = self.__vector.Reverse().Scale(self.__sunpathRadius * self.__sunpathScale)
        # calculate position
        self.__position = self.__sunpathBasePoint.Add(movingVector)
        # create sun sphere
        self.__createSunSphere()

    def __createSunSphere(self):
        """Create the sun sphere"""
        sp = Sphere.ByCenterPointRadius(self.__position, self.scale * self.__sunRadius)
        self.__geometry = sp

    @property
    def vector(self):
        """get sun vector as a Vector"""
        return self.__vector

    @property
    def position(self):
        """get sun position as Point"""
        return self.__position

    @property
    def geometry(self):
        """get sun sphere"""
        return self.__geometry
