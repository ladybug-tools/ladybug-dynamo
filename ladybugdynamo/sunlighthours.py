"""Sunlight hours library for Dynamo"""
from ladybug.listoperations import unflatten
from sunpath import Sun
from analysis import LBAnalysis
import geometryoperations as go


class Sunlighthours(LBAnalysis):
    """Ladybug sunlight hours for Dynamo

        Attributes:
            vectors: A list of sun vectors. Vectors will be flipped during the analysis
            datetimes: A list of LB datetime values with equal length as sun vector
            testPoints: A single list or several lists of test points.
            geometries: A list of all the geometries in scene
    """
    def __init__(self, vectors, datetimes, testPoints, geometries):

        LBAnalysis.__init__(self, vectors, testPoints, geometries)

    @classmethod
    def byTestGeometries(cls, vectors, datetimes, testGeometries, contextGeometries, gridSize, distanceFromBaseSrf):
        # generate test points from geometries
        testPoints = go.generatePointsFromGeometries(testGeometries, gridSize, distanceFromBaseSrf)
        return cls(vectors, datetimes, testPoints, testGeometries + contextGeometries)

    @classmethod
    def bySunsTestPoints(cls, suns, testPoints, contextGeometries):
        """Ladybug sunlight hours for Dynamo

        Args:
            suns: A list of Ladbug suns
            testPoints: A single list or several lists of test points.
            contextGeometries: A list of context geometries
        """
        vectors = range(len(suns))
        datetimes = range(len(suns))
        return cls(vectors, datetimes, testPoints, contextGeometries)

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
        return unflatten([ap.totalNotIntersected for ap in self.analysisPoints])
