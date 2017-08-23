"""Methods for drawing sunpath geometry."""
import clr
clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry as adg


def analemmaCurves(suns, origin, radius):
    """Create analemma curves.

    Args:
        suns: A list of lists of sun positions.
        origin: Sunpath origin.
        radius: Sunpath radius.
    Returns:
        A generator of analemma curves.
    """
    origin = adg.Point.ByCoordinates(*origin)
    for hour in suns:
        try:
            pts = tuple(
                adg.Point.Add(
                    origin,
                    adg.Vector.Scale(
                        adg.Vector.ByCoordinates(
                            sun.sunVector.x, sun.sunVector.y, sun.sunVector.z),
                        -radius))
                for sun in hour)
        except AttributeError:
            # no sun poistion / all night
            continue
        else:
            # create the analemma curve and send it back
            yield adg.NurbsCurve.ByPoints(pts)


def baseCurves(origin, radius, northAngle):
    origin = adg.Point.ByCoordinates(*origin)
    innerCircle = adg.Circle.ByCenterPointRadius(origin, radius)
    middleCircle = adg.Circle.ByCenterPointRadius(origin, 1.02 * radius)
    outterCircle = adg.Circle.ByCenterPointRadius(origin, 1.08 * radius)

    baseCurves = []
    # create North Arrow
    startVector = adg.Vector.Scale(adg.Vector.YAxis(), radius)
    startPt = adg.Point.Add(origin, startVector)
    endVector = adg.Vector.Scale(adg.Vector.YAxis(), 1.12 * radius)
    endPt = adg.Point.Add(origin, endVector)
    northArrow = adg.Line.ByStartPointEndPoint(startPt, endPt)
    # draw it for the 4 direction
    for angle in range(0, 360, 90):
        baseCurves.append(northArrow.Rotate(adg.Plane.XY(),
                                            angle + northAngle))

    # create mid curves
    endVector = adg.Vector.Scale(adg.Vector.YAxis(), 1.08 * radius)
    endPt = adg.Point.Add(origin, endVector)
    shortArrow = adg.Line.ByStartPointEndPoint(startPt, endPt)
    # draw it for the 4 direction
    for angle in range(0, 360, 30):
        if angle % 90 != 0:
            baseCurves.append(
                shortArrow.Rotate(adg.Plane.XY(), angle + northAngle)
            )
    return [innerCircle, middleCircle, outterCircle] + baseCurves


def dailyCurves(suns, origin, radius):
    """Create daily sunpath curves."""
    origin = adg.Point.ByCoordinates(*origin)
    for day, isArc in suns:
        pts = tuple(
            adg.Point.Add(
                origin,
                adg.Vector.Scale(
                    adg.Vector.ByCoordinates(
                        sun.sunVector.x, sun.sunVector.y, sun.sunVector.z),
                    -radius))
            for sun in day)
        if isArc:
            yield adg.Arc.ByThreePoints(*pts)
        else:
            if pts[2].Z > 0:
                yield adg.Circle.ByThreePoints(*pts)


def sunGeometry(suns, origin, radius):
    """Get sun geometries as points."""
    origin = adg.Point.ByCoordinates(*origin)
    return tuple(
        adg.Point.Add(
            origin,
            adg.Vector.Scale(
                adg.Vector.ByCoordinates(
                    sun.sunVector.x, sun.sunVector.y, sun.sunVector.z),
                -radius))
        for sun in suns)
