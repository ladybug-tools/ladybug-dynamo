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

# append ladybug path to sys.path
sys.path.append(getPackagePath('Ladybug'))

###### start you code from here ###
import ladybugdynamo.geometryoperations as go

# Generate test points
surfaces = IN[0] if isinstance(IN[0], list) else [IN[0]]
numOfSegments = IN[1]
distanceFromBaseSrf = IN[2]
pts = []
normals = []

for srf in surfaces:
    p, n = go.generatePointsFromSurface(srf, numOfSegments, distanceFromBaseSrf)
    pts.append(p)
    normals.append(n)
OUT = pts, normals
