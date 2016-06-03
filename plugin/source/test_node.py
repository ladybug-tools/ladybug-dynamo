import sys
p = r"C:\Users\Administrator\AppData\Roaming\Dynamo\Dynamo Revit\1.0\packages\Ladybug\extra\ladybugdynamo"
sys.path.append(p)
#
# from ladybug.analysisperiod import AnalysisPeriod
# from ladybug.epw import EPW
from ladybug.location import Location
from ladybug.sunpath import LBSunpath
# from ladybug.dt import LBDateTime
# from ladybug.datatype import SkyPatch, Temperature, LBData

loc = Location(city='B', latitude=42, longitude=-71)
print repr(loc)
sp = LBSunpath.fromLocation(loc)
for h in range(4109, 4125):
    sun = sp.calculateSunFromHOY(h)
    print sun
