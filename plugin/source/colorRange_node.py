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
import ladybugdynamo.color as color

index = IN[0]
cs = color.LBColorset()
colors = cs[index]
OUT = color.ColorConvertor.toDSColor(colors)
