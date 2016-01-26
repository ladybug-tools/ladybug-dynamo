# add IronPython path to sys
import sys
IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(IronPythonLib)

# Now that the path to IronPython is established we can import libraries
import os
import clr
clr.AddReference('DynamoCore')

def getPackagePath(packageName):
    #Get path to dynamo package using the package name
    dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
    appdata = os.getenv('APPDATA')
    return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

def getDynamoPath():
    return os.path.split(clr.References[2].Location)[0]

# append ladybug path to sys.path
sys.path.append(getPackagePath('Ladybug'))
sys.path.append(getDynamoPath()) #This is for using colors

###### start you code from here ###
import ladybugdynamo.legendparameters as legendpar
from ladybugdynamo.wrapper import Wrapper


# analysis surfaces will be useful for drawing the legend. No use for now.
analysisSurfaces = IN[0]
values = IN[1]

# I couldn't figure out why isinstance(IN[2], Wrapper) returns Flase
# Thta's why I'm using try/exception
#legendPar = IN[2].unwrap() if isinstance(IN[2], Wrapper) else legendpar.LegendParameters()

try:
    legendPar = IN[2].unwrap()
except:
    legendPar = legendpar.LegendParameters()


OUT = legendPar.calculateColors(values)
