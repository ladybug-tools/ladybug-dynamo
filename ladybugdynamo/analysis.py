"""Analysis library for Dynamo.

This calss is base class for radiation and sunlighthours analysis.

WARNING: This class will be replace by honeybee analysis classes in the next
         release.
"""

from abc import ABCMeta, abstractproperty
from ladybug import listoperations as lo
import geometryoperations as go


class LBAnalysis(object):
    """Ladybug base analysis class.

    Attributes:
        vectors: A list of sun vectors. Vectors will be flipped during the analysis
        testPoints: A single list or several lists of test points.
        geometries: A list of all the geometries in scene
    """

    __metaclass__ = ABCMeta

    def __init__(self, vectors, testPoints, geometries, reverseVectors=True,
                 pointsNormal=None, values=None):
        """Init analysis class."""
        # set up the analysis
        # flatten input values
        self.geometries = list(lo.flatten(geometries))
        self.vectors = [vector.Reverse() if reverseVectors else vector for vector in lo.flatten(vectors)]
        self.testPoints = list(lo.flatten(testPoints))
        if pointsNormal:
            self.pointsNormal = list(lo.flatten(pointsNormal))
        else:
            self.pointsNormal = [None] * len(self.testPoints)
        # find maximum length of the scene - which is 3d diagonal
        maxLength = go.calculateSceneSize(self.testPoints + self.geometries)

        # create analysis points
        self.analysisPoints = tuple(go.LBAnalysisPoint(testPoint, self.vectors,
                                                       maxLength,
                                                       self.pointsNormal[count],
                                                       values)
                                    for count, testPoint in enumerate(self.testPoints))

        # create place holder for results
        self.isExecuted = False

    @classmethod
    def bySkyTestPoints(cls):
        """Genrate the analysis by sky and test points."""
        pass

    def runAnalysis(self, parallel=False):
        """Run analysis."""
        for analysisPoint in self.analysisPoints:
            analysisPoint.calculateIntersections(self.geometries, parallel)

        self.isExecuted = True

    # TODO: create meaningful outputs from the analysis
    @abstractproperty
    def results(self):
        """Return results."""
        pass
