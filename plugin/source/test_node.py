# add IronPython path to sys
import sys
IronPythonLib = 'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(IronPythonLib)

# Now that the path to IronPython is established we can import libraries
# import os
# import clr
# clr.AddReference('DynamoCore')
#
# def getPackagePath(packageName):
#     #Get path to dynamo package using the package name
#     dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
#     appdata = os.getenv('APPDATA')
#     return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)
#
# # append ladybug path to sys.path
# sys.path.append(getPackagePath('Ladybug'))
#
# ###### start you code from here ###
# import ladybugdynamo.geometryoperations as go
#
# # This example shows how to calculate sunpath with Ladybug and draw it in Dynamo
# pts = []
# for srf in IN[0]:
#     pts.append(go.generatePointsFromSurface(srf, IN[1], IN[2]))
#
# OUT = pts

# import collections
#
# def flatten(inputList):
#     """Return a flattened genertor from an input list
#
#         Usage:
#             inputList = [['a'], ['b', 'c', 'd'], [['e']], ['f']]
#             list(flatten(inputList))
#             >> ['a', 'b', 'c', 'd', 'e', 'f']
#     """
#     for el in inputList:
#         if isinstance(el, collections.Iterable) and not isinstance(el, basestring):
#             for sub in flatten(el):
#                 yield sub
#         else:
#             yield el
#
# def unflatten(guide, falttenedInput):
#     """Unflatten a falttened generator
#         guide: A guide list to follow the structure
#         falttenedInput: A flattened iterator object
#
#         Usage:
#             guide = [["a"], ["b","c","d"], [["e"]], ["f"]]
#             inputList = [0, 1, 2, 3, 4, 5, 6, 7]
#             unflatten(guide, iter(inputList))
#             >> [[0], [1, 2, 3], [[4]], [5]]
#     """
#     return [unflatten(subList, falttenedInput) if isinstance(subList, list) else next(falttenedInput) for subList in guide]
#
# inputList = [["a"], ["b","c","d"], [["e"]], ["f"]]
# #inputList = [[1,2,3],[4,5,6], [7], [8,9]]
# flattenedList = flatten(inputList)
# print list(flatten(inputList))
# #anotherList = list(flattenedList)
# #unflatten(inputList, anotherList)
# #print unflatten(inputList, iter([0, 1, 2, 3, 4, 5, 6, 7]))
