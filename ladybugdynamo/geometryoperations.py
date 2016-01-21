"""Collection of geometrical operations for Dynamo"""
# import Dynamo libraries
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
from itertools import chain

def disposeGeometries(geometries):
    for geo in geometries: geo.Dispose()

def calculateSceneSize(geometries):
    """Calculate scene size for a list of geometry

        Args:
            geometries: List of input geometries (Solid, Geometry, Points)

        Return:
            length: length of scene's diagonal
    """
    # flatten the list
    flattenedGeometries = list(chain.from_iterable([geometries]))
    bbox = BoundingBox.ByGeometry(flattenedGeometries)
    minPt = bbox.MinPoint
    maxPt = bbox.MaxPoint
    distance = minPt.DistanceTo(maxPt)
    disposeGeometries([bbox, minPt, maxPt])
    return distance

# TODO: Write a proper way to generate test points
def generatePointsFromGeometries(geometries, gridSize, distanceFromBaseSrf):
    pass

# TODO: Add data on top of vectors. It can be timedate or skypatch number
class LBAnalysisPoint:
    """Ladybug Analysis points

        Attributes:
            testPoint: A points that represnts test sensor
            vectors: Test vectors for analysis. It can be sun vectors or vectors for sky patches
            length: maximum length of test secne
    """
    def __init__(self, testPoint, vectors, length):

        self.testPoint = testPoint
        # calculate LinRays
        self.lineRays = [LineRay(self.testPoint, vector, length) for vector in vectors]
        # place holder for intersections
        self.intersections = [False] * len(vectors)

    def calculateIntersections(self, contextGeometries, parallel = False):
        """calculate intersection for this analysis point against conetext geometries"""
        for lineCount, lineRay in enumerate(self.lineRays):
            for geometry in contextGeometries:
                intersection = geometry.Intersect(lineRay.ray)

                if len(intersection) > 0:
                    disposeGeometries(intersection)
                    self.intersections[lineCount] = True
                    break
                else:
                    disposeGeometries(intersection)

        del(self.lineRays)

    @property
    def totalNotIntersected(self):
        return len(self.intersections) - sum(self.intersections)


class LineRay:
    """Create a line ray

        LineRay is useful for solving intersections both for Sunlighthours
        and radition analysis

        Attributes:
            startPoint: A Point that indicated the start point of the ray
            vector: A Vector which the ray should be aimed toward
            length: A float value for the length of the LineRay
    """
    def __init__(self, startPoint, vector, length):
        self.startPoint = startPoint
        self.vector = vector
        self.length = length
        self.ray = self.__calculateRay()

    def __calculateRay(self):
        return Line.ByStartPointDirectionLength(self.startPoint, self.vector, self.length)
