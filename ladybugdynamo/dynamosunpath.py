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

        self.scale = float(scale)
        self.__radius = 50
        self.__suns = [] # placeholder for sun(s)
        self.__dailyCurves = []
        self.__analemmaCurves = []
        self.__baseCurves = []

    @property
    def geometries(self):
        return {
        'suns': self.__suns,
        'dailyCurves': self.__dailyCurves,
        'analemmaCurves': self.__analemmaCurves,
        'baseCurves': self.__baseCurves
        }

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

    @property
    def suns(self):
        """Get list of suns"""
        return self.__suns

    def addSun(self, sun):
        """Add a new sun to sunpath"""
        assert type(sun) == Sun
        self.__suns.append(sun)

    def removeSuns(self):
        """Remove all suns from the sunpath"""
        self.__suns = []
        return True

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
        DSSunVector = DSSunVector.Reverse().Scale(self.__radius)
        sunPosition = self.basePoint.Add(DSSunVector)

        return sunPosition, sun.isDuringDay

    def calculateSun(self, month, day, hour, isSolarTime = False):
        pass

    def calculateSunFromHOY(self, HOY, isSolarTime = False):
        pass

    def calculateSunFromDateTime(self, datetime, isSolarTime = False):
        pass

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
            sunPos, isDay = self.calculateSunPositionFromDateTime(datetime, isSolarTime = False)
            dailySunPositions.append(sunPos)

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
        for hour in range(1, 25):
            monthlySunPositions = []
            for month in range(1,13):
                sunPos, isDay = self.calculateSunPosition(month, day, hour = hour)
                if isDay:
                    monthlySunPositions.append(sunPos)
                else:
                    continue
                    # calculate sunset or sunrise and append that position
                    dts = self.sunPath.calculateSunriseSunset(month, day, depression = 0, isSolarTime = False)

                    if hour > 12:
                        shour = dts['sunset'].floatHour
                    else:
                        shour = dts['sunrise'].floatHour

                    sunPos, isDay = self.calculateSunPosition(month, day, shour)
                    monthlySunPositions.append(sunPos)

            if len(monthlySunPositions) > 1:
                analemmaCurve = NurbsCurve.ByPoints(monthlySunPositions, True)
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
