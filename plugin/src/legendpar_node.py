# assign inputs
_domain_, _cType_, _colors_ = IN
legendPar = None

try:
    import ladybug.legendparameters as lpar
    import ladybug.color as col
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

legendPar = lpar.LegendParameters(
    legend_range=_domain_, number_of_segments=11,
    colors=_colors_, chart_type=_cType_
)

# assign outputs to OUT
OUT = (legendPar,)