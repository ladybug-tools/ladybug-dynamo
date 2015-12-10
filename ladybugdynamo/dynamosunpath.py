import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import math

class DSSunpath:
    """
    Calculates sun path for Dynamo

    Attributes:
        sunPath: ladybug Sunpath
        basePoint: A DS point that will be used as the center of sunpath. Default is Origin
        scale: A number larger than 0 for scale of sunpath
        sunScale: A number larger than 0 for scale of sun spheres

    Usage:
        import ladybug.epw as epw
        import ladybug.sunpath as sunpath
        import ladybugdynamo.dynamosunpath as dssunpath

        # initiate sunpath based on location
        sp = sunpath.Sunpath.fromLocation(locationData)
        dynamoSp = dssunpath.DSSunpath(sp)
        hourlyCurves = dynamoSp.drawSunPath()
    """

    def __init__(self, sunPath, basePoint = None, scale = 1, sunScale = 1):
        # print type(sunPath)
        #assert type(sunPath) == Sunpath
        self.sunPath = sunPath

        if not basePoint: basePoint = Point.Origin()
        self.basePoint = Point.ByCoordinates(basePoint.X, basePoint.Y, basePoint.Z)

        self.scale = float(scale) #scale of the whole sunpath
        self.sunScale = float(sunScale) * self.scale #scale for sun s
        self.__sunRadius = 1
        self.__radius = 50
        self.__suns = [] # placeholder for sun(s)
        self.__dailyCurves = []
        self.__analemmaCurves = []
        self.__baseCurves = []

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

        if sun.isDuringDay:
            self.__createSunSphere(sun) #it will be added to sun itself
            self.__suns.append(sun)

    def drawSunFromDateTime(self, dateTime, isSolarTime = False):
        """Draw a sun based on datetime"""
        self.drawSun(dateTime.month, dateTime.day, dateTime.floatHour, isSolarTime)

    def __createSunSphere(self, sun):
        """Create an sphere and add it to sun.geometry"""
        sp = Sphere.ByCenterPointRadius(sun.position, self.sunScale * self.__sunRadius)
        sun.geometry = sp

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
                sunPosition: A DSPoint that represnts sun position in model
                isDuringDay: A boolean that indicates if sun position is above the horizon
        """
        return self.calculateSunPosition(dateTime.month, dateTime.day, dateTime.floatHour, isSolarTime)

    def calculateSunPosition(self, month = 12, day = 21, hour = 12, isSolarTime = False):
        """ Calculate the position of sun based on origin and scale

            Returns:
                sunPosition: A DSPoint that represnts sun position in model
                isDuringDay: A boolean that indicates if sun position is above the horizon
        """
        # calculate sun for this time
        sun = self.sunPath.calculateSun(month, day, hour, isSolarTime)

        # calculate sunposition
        DSSunVector = Vector.ByCoordinates(sun.sunVector.x, \
            sun.sunVector.y, sun.sunVector.z)
        DSSunVector = DSSunVector.Reverse().Scale(self.__radius * self.scale)

        sun.vector = DSSunVector
        sun.position = self.basePoint.Add(DSSunVector)

        return sun

    def calculateDailyCurve(self, month, day = 21, isSolarTime = False):
        """Calculate daily curve the day
            After calculating the curves check 'dailyCurves' property for curve geometries
        """
        # calculate sunrise, noon and sunset
        datetimesDictionary = self.sunPath.calculateSunriseSunset(month, day = day, depression = 0, isSolarTime = isSolarTime)

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
                # join curves
                    analemmaCurve = selectedCurves[0].Join(selectedCurves[1:])

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
            self.__baseCurves.append(northArrow.Rotate(Plane.XY(), angle))

        # create mid curves
        endVector = Vector.Scale(Vector.YAxis(), 1.08 * self.scale * self.__radius)
        endPt = Point.Add(self.basePoint, endVector)
        shortArrow = Line.ByStartPointEndPoint(startPt, endPt)
        # draw it for the 4 direction
        for angle in range(0, 360, 30):
            if angle%90!=0:
                self.__baseCurves.append(shortArrow.Rotate(Plane.XY(), angle))

    def __drawBaseCircles(self):
        """draw base circles"""
        innerCircle = Circle.ByCenterPointRadius(self.basePoint, self.scale * self.__radius)
        outerCircle = Circle.ByCenterPointRadius(self.basePoint, 1.02 * self.scale * self.__radius)
        outerCircle2 = Circle.ByCenterPointRadius(self.basePoint, 1.08 * self.scale * self.__radius)
        self.__baseCurves.extend([outerCircle, innerCircle, outerCircle2])
