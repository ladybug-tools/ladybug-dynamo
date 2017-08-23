import clr
clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as dg


def point(x, y, z):
    """Point 3d by x, y ,z."""
    return dg.Point.ByCoordinates(x, y, z)


def origin():
    """Origin point."""
    return dg.Point.Origin()


def arc(startPoint, midPoint, endPoint):
    """Arc by 3 points."""
    spt = dg.Point.ByCoordinates(*startPoint)
    mpt = dg.Point.ByCoordinates(*midPoint)
    ept = dg.Point.ByCoordinates(*endPoint)
    arc = dg.Arc.ByThreePoints(spt, mpt, ept)
    spt.Dispose()
    mpt.Dispose()
    ept.Dispose()
    return arc


def plane(pt, normal):
    """Plane by center (x, y, z) and normal (x, y, z)."""
    dg.Plane.ByOriginNormal(
        dg.Point.ByCoordinates(*pt), dg.Vector.ByCoordinates(*normal))


def line(startPoint, endPoint):
    """Line by start and end point (x, y, z)."""
    spt = dg.Point.ByCoordinates(*startPoint)
    ept = dg.Point.ByCoordinates(*endPoint)
    ln = dg.Line.ByStartPointEndPoint(spt, ept)
    spt.Dispose()
    ept.Dispose()
    return ln


def circle(centerPoint, radius):
    """Circle from centerPoint and radius."""
    cenpt = dg.Point.ByCoordinates(*centerPoint)
    cir = dg.Circle.ByCenterPointRadius(cenpt, radius)
    cenpt.Dispose()
    return cir


def curve(points):
    """Curve from collection of points."""
    pts = tuple(dg.Point.ByCoordinates(*pt) for pt in points)
    crv = dg.NurbsCurve.ByPoints(pts, True)
    for pt in pts:
        pt.Dispose()
    return crv


def sphere(centerPoint, radius):
    """Sphere by center point and radius."""
    cenpt = dg.Point.ByCoordinates(*centerPoint)
    sp = dg.Sphere.ByCenterPointRadius(cenpt, radius)
    cenpt.Dispose()
    return sp


def vector(x, y, z):
    """Vector by x, y, z."""
    return dg.Vector.ByCoordinates(x, y, z)


def trim(geometry, plane, pt):
    """Trim curve by plane."""
    return dg.Geometry.Trim(geometry, plane, pt)


def trimCurveByPlane(geometry, plane, pt):
    """Trim curve by plane.

    All the inputs should be Dynamo geometry.
    """

    curves = dg.Geometry.Trim(geometry, plane, pt)
    # Dynamo trim doesn't work as expected
    # or I don't know how it is supposed to work so I check the curves
    selectedCurves = []
    for curve in curves:
        # find mid point
        midPar = (curve.EndParameter() + curve.StartParameter()) / 2
        midPt = curve.PointAtParameter(midPar)
        if midPt.Z >= 0:
            selectedCurves.append(curve)
        else:
            curve.Dispose()

    if len(selectedCurves) == 1:
        analemmaCurve = selectedCurves[0]
    else:
        try:
            # join curves
            analemmaCurve = selectedCurves[0].Join(selectedCurves[1:])
        except StandardError:
            analemmaCurve = selectedCurves

    return analemmaCurve
