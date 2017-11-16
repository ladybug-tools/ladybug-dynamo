"""Methods for drawing sunpath geometry."""
try:
    import clr
    clr.AddReference('ProtoGeometry')
    import Autodesk.DesignScript.Geometry as adg
except ImportError:
    pass


def analemma_curves(suns, origin, radius):
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
                            sun.sun_vector.x, sun.sun_vector.y, sun.sun_vector.z),
                        -radius))
                for sun in hour)
        except AttributeError:
            # no sun poistion / all night
            continue
        else:
            # create the analemma curve and send it back
            yield adg.NurbsCurve.ByPoints(pts)


def base_curves(origin, radius, north_angle):
    origin = adg.Point.ByCoordinates(*origin)
    inner_circle = adg.Circle.ByCenterPointRadius(origin, radius)
    middle_circle = adg.Circle.ByCenterPointRadius(origin, 1.02 * radius)
    outter_circle = adg.Circle.ByCenterPointRadius(origin, 1.08 * radius)

    base_curves = []
    # create North Arrow
    start_vector = adg.Vector.Scale(adg.Vector.YAxis(), radius)
    start_pt = adg.Point.Add(origin, start_vector)
    end_vector = adg.Vector.Scale(adg.Vector.YAxis(), 1.12 * radius)
    end_pt = adg.Point.Add(origin, end_vector)
    north_arrow = adg.Line.ByStartPointEndPoint(start_pt, end_pt)
    # draw it for the 4 direction
    for angle in range(0, 360, 90):
        base_curves.append(north_arrow.Rotate(adg.Plane.XY(),
                                              angle + north_angle))

    # create mid curves
    end_vector = adg.Vector.Scale(adg.Vector.YAxis(), 1.08 * radius)
    end_pt = adg.Point.Add(origin, end_vector)
    short_arrow = adg.Line.ByStartPointEndPoint(start_pt, end_pt)
    # draw it for the 4 direction
    for angle in range(0, 360, 30):
        if angle % 90 != 0:
            base_curves.append(
                short_arrow.Rotate(adg.Plane.XY(), angle + north_angle)
            )
    return [inner_circle, middle_circle, outter_circle] + base_curves


def daily_curves(suns, origin, radius):
    """Create daily sunpath curves."""
    origin = adg.Point.ByCoordinates(*origin)
    for day, is_arc in suns:
        pts = tuple(
            adg.Point.Add(
                origin,
                adg.Vector.Scale(
                    adg.Vector.ByCoordinates(
                        sun.sun_vector.x, sun.sun_vector.y, sun.sun_vector.z),
                    -radius))
            for sun in day)
        if is_arc:
            yield adg.Arc.ByThreePoints(*pts)
        else:
            if pts[2].Z > 0:
                yield adg.Circle.ByThreePoints(*pts)


def sun_geometry(suns, origin, radius):
    """Get sun geometries as points."""
    origin = adg.Point.ByCoordinates(*origin)
    return tuple(
        adg.Point.Add(
            origin,
            adg.Vector.Scale(
                adg.Vector.ByCoordinates(
                    sun.sun_vector.x, sun.sun_vector.y, sun.sun_vector.z),
                -radius))
        for sun in suns)
