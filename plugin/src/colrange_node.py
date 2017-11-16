# assign inputs
_index = IN[0]
colors = None

try:
    import ladybug.color as col
    import ladybug.output as output
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

_index = _index or 0
cs = col.Colorset()
colors = output.color_to_color(cs[_index])


# assign outputs to OUT
OUT = (colors,)