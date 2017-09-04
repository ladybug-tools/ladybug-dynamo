try:
    import clr
    clr.AddReference('ProtoGeometry')
    import Autodesk.DesignScript.Geometry as dg
except ImportError:
    pass


def point(x, y, z):
    """Point 3d by x, y ,z."""
    return dg.Point.ByCoordinates(x, y, z)


def origin():
    """Origin point."""
    return dg.Point.Origin()


def arc(start_point, mid_point, end_point):
    """Arc by 3 points."""
    spt = dg.Point.ByCoordinates(*start_point)
    mpt = dg.Point.ByCoordinates(*mid_point)
    ept = dg.Point.ByCoordinates(*end_point)
    arc = dg.Arc.ByThreePoints(spt, mpt, ept)
    spt.Dispose()
    mpt.Dispose()
    ept.Dispose()
    return arc


def plane(pt, normal):
    """Plane by center (x, y, z) and normal (x, y, z)."""
    dg.Plane.ByOriginNormal(
        dg.Point.ByCoordinates(*pt), dg.Vector.ByCoordinates(*normal))


def line(start_point, end_point):
    """Line by start and end point (x, y, z)."""
    spt = dg.Point.ByCoordinates(*start_point)
    ept = dg.Point.ByCoordinates(*end_point)
    ln = dg.Line.ByStartPointEndPoint(spt, ept)
    spt.Dispose()
    ept.Dispose()
    return ln


def circle(center_point, radius):
    """Circle from center_point and radius."""
    cenpt = dg.Point.ByCoordinates(*center_point)
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


def sphere(center_point, radius):
    """Sphere by center point and radius."""
    cenpt = dg.Point.ByCoordinates(*center_point)
    sp = dg.Sphere.ByCenterPointRadius(cenpt, radius)
    cenpt.Dispose()
    return sp


def vector(x, y, z):
    """Vector by x, y, z."""
    return dg.Vector.ByCoordinates(x, y, z)


def trim(geometry, plane, pt):
    """Trim curve by plane."""
    return dg.Geometry.Trim(geometry, plane, pt)


def trim_curve_by_plane(geometry, plane, pt):
    """Trim curve by plane.

    All the inputs should be Dynamo geometry.
    """

    curves = dg.Geometry.Trim(geometry, plane, pt)
    # Dynamo trim doesn't work as expected
    # or I don't know how it is supposed to work so I check the curves
    selected_curves = []
    for curve in curves:
        # find mid point
        mid_par = (curve.EndParameter() + curve.StartParameter()) / 2
        mid_pt = curve.PointAtParameter(mid_par)
        if mid_pt.Z >= 0:
            selected_curves.append(curve)
        else:
            curve.Dispose()

    if len(selected_curves) == 1:
        analemma_curve = selected_curves[0]
    else:
        try:
            # join curves
            analemma_curve = selected_curves[0].Join(selected_curves[1:])
        except Exception:
            analemma_curve = selected_curves

    return analemma_curve
