"""Sunlight hours library for Dynamo."""
from ladybug.listoperations import unflatten
from analysis import LBAnalysis
import geometryoperations as go


class SolarRadiation(LBAnalysis):
    """Ladybug sunlight hours for Dynamo.

    Attributes:
        sky: A Ladybug sky
        testPoints: A single list or several lists of test points.
        geometries: A list of all the geometries in scene.
    """

    # TODO: add a classmethod to LBAnalysis for running the analysis from
    # skyTotalRadiation radiation values and vectors should be unwrapped in LBAnalysis
    def __init__(self, sky, testPoints, pointsNormal, geometries):
        """Init class."""
        self.__guideList = testPoints
        self.__raditionValues = sky.skyTotalRadiation.values(header=False)
        # generate vectors from sky
        vectors = [go.toDSVector(r.vector) for r in self.__raditionValues]
        LBAnalysis.__init__(self, vectors, testPoints, geometries,
                            reverseVectors=False, pointsNormal=pointsNormal,
                            values=self.__raditionValues)

    def runAnalysis(self, parallel=False):
        """Run the analysis."""
        for analysisPoint in self.analysisPoints:
            analysisPoint.calculateIntersections(self.geometries, parallel)

        self.isExecuted = True

    # TODO: create meaningful outputs from the analysis
    @property
    def results(self):
        """Return results of the analysis."""
        if not self.isExecuted:
            self.runAnalysis(parallel=True)

        # package the results and return the package
        # return [[line.ray for line in ap.lineRays] for ap in self.analysisPoints]
        # return [ap.intersections for ap in self.analysisPoints]
        return unflatten(self.__guideList,
                         (ap.totalNotIntersected for ap in self.analysisPoints))
