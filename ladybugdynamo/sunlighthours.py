"""Sunlight hours library for Dynamo"""
from ladybugdynamo.sunpath import Sun
import ladybugdynamo.geometryoperations as go


class Sunlighthours:
    """Ladybug sunlight hours for Dynamo

        Attributes:
            vectors: A list of sun vectors. Vectors will be flipped during the analysis
            datetimes: A list of LB datetime values with equal length as sun vector
            testPoints: A single list or several lists of test points.
            geometries: A list of all the geometries in scene
    """
    def __init__(self, vectors, datetimes, testPoints, geometries):
        # set up the analysis
        self.geometries = geometries
        self.vectors = [vector.Reverse() for vector in vectors]
        # find maximum length of the scene - which is 3d diagonal
        maxLength = go.calculateSceneSize(testPoints + geometries)

        # create analysis points
        self.analysisPoints = [go.LBAnalysisPoint(testPoint, self.vectors, maxLength) for testPoint in testPoints]

        # create place holder for results
        self.isExecuted = False

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
        return [ap.totalNotIntersected for ap in self.analysisPoints]
