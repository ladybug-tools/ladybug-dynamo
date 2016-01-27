# add IronPython path to sys
import sys
IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(IronPythonLib)

# Now that the path to IronPython is established we can import libraries
# I don't need them in this case but just for testing memory
import os
import clr
clr.AddReference('DynamoCore')
import copy

def getPackagePath(packageName):
    #Get path to dynamo package using the package name
    dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
    appdata = os.getenv('APPDATA')
    return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

# append ladybug path to sys.path
sys.path.append(getPackagePath('Ladybug'))

###### start you code from here ###
from ladybugdynamo.wrapper import Wrapper
import ladybugdynamo.sky as sky

# get input data
epwfile = IN[0]
skyDensity = IN[1]
workingDir = IN[2] if IN[2].strip()!="" else os.path.join(getPackagePath('Ladybug') + "temp\\cumulativeSkies")

cSky = sky.CumulativeSkyMtx(epwfile,  skyDensity= skyDensity, workingDir = workingDir)

try:
    cSky.gendaymtx(pathToRadianceBinaries = os.path.join(getPackagePath('Ladybug'), "bin"))
    # assign sky to output
    OUT = Wrapper(cSky)
except Exception, e:
    OUT = str(e)
