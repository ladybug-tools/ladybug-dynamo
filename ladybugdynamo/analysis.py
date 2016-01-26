"""Analysis library for Dynamo. This calss is base class for radiation and sunlighthours analysis"""
from abc import ABCMeta, abstractmethod, abstractproperty
from ladybug import listoperations as lo
import geometryoperations as go

class LBAnalysis(object):
    """Ladybug base analysis class

        Attributes:
            vectors: A list of sun vectors. Vectors will be flipped during the analysis
            testPoints: A single list or several lists of test points.
            geometries: A list of all the geometries in scene
    """
    def __init__(self, vectors, testPoints, geometries):
        # set up the analysis
        # flatten input values
        self.geometries = lo.flatten(geometries)
        self.vectors = [vector.Reverse() for vector in lo.flatten(vectors)]

        # find maximum length of the scene - which is 3d diagonal
        maxLength = go.calculateSceneSize(testPoints + geometries)

        # create analysis points
        self.analysisPoints = [go.LBAnalysisPoint(testPoint, self.vectors, maxLength) \
            for testPoint in lo.flatten(testPoints)]

        # create place holder for results
        self.isExecuted = False

    def runAnalysis(self, parallel = False):
        for analysisPoint in self.analysisPoints:
            analysisPoint.calculateIntersections(self.geometries, parallel)

        self.isExecuted = True

    #TODO: create meaningful outputs from the analysis
    @abstractproperty
    def results(self):
        pass
