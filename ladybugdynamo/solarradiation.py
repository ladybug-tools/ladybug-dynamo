"""Sunlight hours library for Dynamo"""
from ladybug.listoperations import unflatten
from sunpath import Sun
from analysis import LBAnalysis
import geometryoperations as go


class SolarRadiation(LBAnalysis):
    """Ladybug sunlight hours for Dynamo

        Attributes:
            sky: A Ladybug sky
            testPoints: A single list or several lists of test points.
            geometries: A list of all the geometries in scene
    """
    def __init__(self, sky, testPoints, geometries):
        self.__guideList = testPoints
        LBAnalysis.__init__(self, vectors, testPoints, geometries)

    @classmethod
    def byTestGeometries(cls, sky, testGeometries, contextGeometries, gridSize, distanceFromBaseSrf):
        # generate test points from geometries
        #testPoints = go.generatePointsFromGeometries(testGeometries, gridSize, distanceFromBaseSrf)
        #return cls(vectors, datetimes, testPoints, testGeometries + contextGeometries)
        raise NotImplementedError()

    @classmethod
    def bySkyTestPoints(cls, sky, testPoints, contextGeometries):
        """Ladybug sunlight hours for Dynamo

        Args:
            suns: A list of Ladbug suns
            testPoints: A single list or several lists of test points.
            contextGeometries: A list of context geometries
        """
        # vectors = range(len(suns))
        # datetimes = range(len(suns))
        # return cls(vectors, datetimes, testPoints, contextGeometries)
        raise NotImplementedError()

    @classmethod
    def bySunsTestGeometries(cls, suns, testGeometries, contextGeometries, gridSize, distanceFromBaseSrf):

        # generate test points from geometries
        testPoints = go.generatePointsFromGeometries(testGeometries, gridSize, distanceFromBaseSrf)
        return cls.bySunsTestPoints(suns, testPoints, testGeometries + contextGeometries)


    def runAnalysis(self, parallel = False):
        for analysisPoint in self.analysisPoints:
            analysisPoint.calculateIntersections(self.geometries, parallel)

        self.isExecuted = True

    #TODO: create meaningful outputs from the analysis
    @property
    def results(self):
        """Return results of the analysis"""
        if not self.isExecuted:
            self.runAnalysis(parallel = True)

        # package the results and return the package
        #return [[line.ray for line in ap.lineRays] for ap in self.analysisPoints]
        #return [ap.intersections for ap in self.analysisPoints]
        return unflatten(self.__guideList, iter([ap.totalNotIntersected for ap in self.analysisPoints]))
