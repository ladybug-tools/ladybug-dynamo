# assign inputs
_values, legendPar_ = IN
colors = None

try:
    import ladybug.legendparameters as lpar
    import ladybug.output as output
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _values:
    legendPar = legendPar_ or lpar.LegendParameters()
    colors = output.colorTocolor(legendPar.calculateColors(_values))


# assign outputs to OUT
OUT = (colors,)