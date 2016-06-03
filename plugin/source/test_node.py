import sys
p = r"C:\Users\Administrator\AppData\Roaming\Dynamo\Dynamo Revit\1.0\packages\Ladybug\extra\ladybugdynamo"
sys.path.append(p)
#
# from ladybug.analysisperiod import AnalysisPeriod
# from ladybug.epw import EPW
# from ladybug.sunpath import LBSun
# from ladybug.dt import LBDateTime
# from ladybug.datatype import SkyPatch, Temperature, LBData
from ladybug.sky import CumulativeSkyMtx
from time import time

t= time()
epwfile = r"C:\EnergyPlusV8-3-0\WeatherData\USA_CO_Golden-NREL.724666_TMY3.epw"
cSky = CumulativeSkyMtx(epwfile, skyDensity=0, workingDir=r"c:\ladybug\ dynamo test")
# cSky.gendaymtx(pathToRadianceBinaries=r"c:\radiance\bin")
cSky.gendaymtx(diffuse=True, direct=True,
               analysisPeriod=range(8759))
print cSky.skyTotalRadiation
