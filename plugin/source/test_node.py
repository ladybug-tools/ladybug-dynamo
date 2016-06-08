import sys
p = r"C:\Users\Administrator\AppData\Roaming\Dynamo\Dynamo Revit\1.0\packages\Ladybug\extra\ladybugdynamo"
sys.path.append(p)
#

from ladybug.analysisperiod import AnalysisPeriod

# from ladybug.epw import EPW
# from ladybug.location import Location
# from ladybug.sunpath import LBSunpath
# from ladybug.dt import LBDateTime
# from ladybug.datatype import SkyPatch, Temperature, LBData
ap = AnalysisPeriod(stMonth=12, stDay=31,
                    endMonth=1, endDay=1,
                    timestep=2)

print ap.datetimes
