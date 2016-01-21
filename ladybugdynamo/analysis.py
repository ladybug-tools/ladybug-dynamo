"""Analysis library for Dynamo. This calss is base class for radiation and sunlighthours analysis"""
import geometryoperations as go

class LBAnalysis:
    """Ladybug base analysis class

        Attributes:
            vectors: A list of sun vectors. Vectors will be flipped during the analysis
            testPoints: A single list or several lists of test points.
            geometries: A list of all the geometries in scene
    """
    def __init__(self, vectors, testPoints, geometries):
        # set up the analysis
        self.geometries = geometries
        self.vectors = [vector.Reverse() for vector in vectors]

        # find maximum length of the scene - which is 3d diagonal
        maxLength = go.calculateSceneSize(testPoints + geometries)

        # create analysis points
        self.analysisPoints = [go.LBAnalysisPoint(testPoint, self.vectors, maxLength) for testPoint in testPoints]

        # create place holder for results
        self.isExecuted = False

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
