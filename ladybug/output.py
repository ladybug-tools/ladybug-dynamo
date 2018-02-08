"""Collection of methods for dealing with outputs in Dynamo."""
try:
    # import Dynamo libraries
    import clr
    clr.AddReference("DSCoreNodes")
    from DSCore import Color as DSColor
except ImportError:
    pass


def wrap(input):
    """Replicate method for Grashopper library.

    This is a workaround  to use th exact same code in bot libraries.
    """
    return input


def list_to_tree(input):
    """Replicate method for Grashopper library.

    This is a workaround  to use th exact same code in bot libraries.
    """
    return input


def color_to_color(colors):
    """Convert a ladybug color into Dynamo color."""
    if not hasattr(colors, '__iter__'):
        colors = (colors,)
    try:
        return tuple(DSColor.ByARGB(255, col.r, col.g, col.b) for col in colors)
    except AttributeError as e:
        raise AttributeError('Inputs must be of type of Color:\n{}'.format(e))
