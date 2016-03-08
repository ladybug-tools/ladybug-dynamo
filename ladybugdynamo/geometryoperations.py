"""Collection of geometrical operations for Dynamo"""
# import Dynamo libraries
try:
    import clr
    clr.AddReference('ProtoGeometry')
    from Autodesk.DesignScript.Geometry import *
except ImportError:
    print "Failed to import Dynamo libraries. Make sure path is added to sys.path"
from ladybug.listoperations import *
import math

def toDSVector(vector):
    try:
        return Vector.ByCoordinates(vector.x, vector.y, vector.z)
    except:
        return Vector.ByCoordinates(*vector)

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
    for geo in geometries:
        assert isinstance(geo, Geometry), \
            "%s is not a geometry"%str(geo)
    bbox = BoundingBox.ByGeometry(geometries)
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
    __ptNormals = []
    for p in parameters:
        pts = []
        normals = []
        for pp in parameters:
            uv = UV.ByCoordinates(p, pp)
            pt = testSurface.PointAtParameter(uv.U, uv.V)
            normal = testSurface.NormalAtParameter(uv.U, uv.V).Normalized().Scale(distanceFromBaseSrf)
            pts.append(pt.Translate(normal))
            normals.append(normal)

        __pts.append(pts)
        __ptNormals.append(normals)
    return __pts, __ptNormals

# TODO: Add data on top of vectors. It can be timedate or skypatch number
class LBAnalysisPoint:
    """Ladybug Analysis points

        Attributes:
            testPoint: A points that represnts test sensor
            vectors: Test vectors for analysis. It can be sun vectors or vectors for sky patches
            length: maximum length of test secne
            pointNormal: A vector that represents test point's directon. None for sunlighthours analysisPoint
            values: A list of values that correspond to the list of vectors. None for sunlighthours analysis
    """
    def __init__(self, testPoint, vectors, length, pointNormal = None, values = None):

        self.testPoint = testPoint
        # calculate LinRays
        self.lineRays = [LineRay(self.testPoint, vector, length) for vector in vectors]
        # angle between test point normal and vectors. If no point normal angle is set to 0
        self.angles = [pointNormal.AngleBetween(vector) if pointNormal else 0 for vector in vectors]
        # values for each vectors. If no value it will be set to 1
        self.values = values if values else [1] * len(vectors)
        # assume that point sees none of the vectors
        self.intensity = [0] * len(vectors)

    def calculateIntersections(self, contextGeometries, parallel = False):
        """calculate intersection for this analysis point against conetext geometries"""
        for lineCount, lineRay in enumerate(self.lineRays):
            # in case angle is larger than 90 or vector value is 0 result will
            # be 0 - continue to next line ray
            if self.angles[lineCount] >= 90 or self.values[lineCount] == 0:
                continue

            for geometry in contextGeometries:
                intersection = geometry.Intersect(lineRay.ray)

                if len(intersection) > 0:
                    disposeGeometries(intersection)
                    self.intensity[lineCount] = 0
                    break
                else:
                    disposeGeometries(intersection)
                    # calculate value based on normal angle and value
                    self.intensity[lineCount] = \
                        self.values[lineCount] * math.cos(math.radians(self.angles[lineCount]))

        #dispose lineRays
        for lr in self.lineRays:
            disposeGeometries([lr.ray])
        del(self.lineRays)

    @property
    def totalNotIntersected(self):
        return sum(self.intensity)

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
