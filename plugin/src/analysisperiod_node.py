# assign inputs
_startMonth_, _startDay_, _startHour_, _endMonth_, _endDay_, _endHour_, _timestep_ = IN
analysisPeriod = hoys = dates = None

try:
    import ladybug.analysisperiod as ap
    import ladybug.output as output
except ImportError as e:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

anp = ap.AnalysisPeriod(
    _startMonth_, _startDay_, _startHour_,
    _endMonth_, _endDay_, _endHour_, _timestep_)

if anp:
    analysisPeriod = anp
    dates = output.wrap(anp.datetimes)
    hoys = output.wrap(anp.hoys)

# assign outputs to OUT
OUT = analysisPeriod, hoys, dates