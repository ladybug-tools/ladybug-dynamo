"""Collection of geometrical operations for Dynamo"""
# import Dynamo libraries
import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
import collections

def flatten(inputList):
    """Return a flattened genertor from an input list

        Usage:
            inputList = [['a'], ['b', 'c', 'd'], [['e']], ['f']]
            list(flatten(inputList))
            >> ['a', 'b', 'c', 'd', 'e', 'f']
    """
    for el in inputList:
        if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
            for sub in flatten(el):
                yield sub
        else:
            yield el

def unflatten(guide, falttenedInput):
    """Unflatten a falttened generator
        guide: A guide list to follow the structure
        falttenedInput: A flattened iterator object

        Usage:
            guide = [["a"], ["b","c","d"], [["e"]], ["f"]]
            inputList = [0, 1, 2, 3, 4, 5, 6, 7]
            unflatten(guide, iter(inputList))
            >> [[0], [1, 2, 3], [[4]], [5]]
    """
    return [unflatten(subList, falttenedInput) if isinstance(subList, list) else next(falttenedInput) for subList in guide]

def disposeGeometries(geometries):
    try:
        for geo in geometries: geo.Dispose()
    except Exception, e:
        print str(e)

def calculateSceneSize(geometries):
    """Calculate scene size for a list of geometry

        Args:
            geometries: List of input geometries (Solid, Geometry, Points)

        Return:
            length: length of scene's diagonal
    """
    # flatten the list
    flattenedGeometries = list(flatten([geometries]))
    bbox = BoundingBox.ByGeometry(flattenedGeometries)
    minPt = bbox.MinPoint
    maxPt = bbox.MaxPoint
    distance = minPt.DistanceTo(maxPt)
    disposeGeometries([bbox, minPt, maxPt])
    return distance

def xfrange(start, stop, step):
    values = []
    while start <= stop:
        values.append(start)
        start += step

    return values

# TODO: Change numberOfSegments to gridSize
def generatePointsFromSurface(testSurface, numOfSegments, distanceFromBaseSrf):
    #generate values between 0 and 1 based on number of segments
    step = 1.0 / (numOfSegments - 1)
    parameters = xfrange(0.00, 1.00, step)
    __pts = []
    for p in parameters:
        pts = []
        for pp in parameters:
            uv = UV.ByCoordinates(p, pp)
            pt = testSurface.PointAtParameter(uv.U, uv.V)
            normal = testSurface.NormalAtParameter(uv.U, uv.V).Normalized().Scale(distanceFromBaseSrf)
            pts.append(pt.Translate(normal))

        __pts.append(pts)

    return __pts

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