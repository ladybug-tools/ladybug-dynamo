# assign inputs
_domain_, _cType_, _colors_ = IN
legendPar = None

try:
    import ladybug.legendparameters as lpar
    import ladybug.color as col
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

legendPar = lpar.LegendParameters(
    legendRange=_domain_, numberOfSegments=11,
    colors=_colors_, chartType=_cType_
)

# assign outputs to OUT
OUT = (legendPar,)