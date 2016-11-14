# ##### start you code from here ###

# import Ladybug libraries
from ladybugdynamo.analysisperiod import AnalysisPeriod

# assign inputs from dynamo python node
# I have to export it as a string in Dynamo since inputs can't handle type casting
ap = AnalysisPeriod(*IN)
dates = ap.datetimes
hoys = ap.HOYs
OUT = ap, dates, hoys
