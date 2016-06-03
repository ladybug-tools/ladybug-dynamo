# try:
# add IronPython path to sys
import sys
IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(IronPythonLib)

# Now that the path to IronPython is established we can import libraries
import os
import clr
clr.AddReference('DynamoCore')

def getPackagePath(packageName):
    """Get path to dynamo package using the package name."""
    _loc = clr.References[2].Location
    _ver = _loc.split('\\')[-2].split(' ')[-1]

    # the path structure has changed after the release of version 1
    dynamoPath_1 = "Dynamo\\Dynamo Revit\\" + _ver
    dynamoPath_0 = "Dynamo\\" + _ver
    appdata = os.getenv('APPDATA')
    path1 = '%s\%s\packages\%s\extra\\' % (appdata, dynamoPath_1, packageName)
    path0 = '%s\%s\packages\%s\extra\\' % (appdata, dynamoPath_0, packageName)

    if os.path.isdir(path1):
        return path1
    elif os.path.isdir(path0):
        return path0
    else:
        raise Exception("Can't find Dynamo installation Folder!")

def getDynamoPath():
    return os.path.split(clr.References[2].Location)[0]

# append ladybug path to sys.path
sys.path.append(getPackagePath('Ladybug'))
sys.path.append(getDynamoPath())  # This is for using colors

###### start you code from here ###
import ladybugdynamo.legendparameters as legendpar

# analysis surfaces will be useful for drawing the legend. No use for now.
analysisSurfaces = IN[0]
values = IN[1]
legendPar = IN[2] if IN[2] else legendpar.LegendParameters()

OUT = legendPar.calculateColors(values)

# except Exception, e:
#     OUT = "ERROR:\n%s" % str(e) + \
#         "\nIf you think this is a bug submit an issue on github.\n" + \
#         "https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
