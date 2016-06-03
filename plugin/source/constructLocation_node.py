try:
    """
    # Construct location
    #
    # Ladybug: A Plugin for Environmental Analysis (GPL) started by Mostapha Sadeghipour Roudsari
    #
    # This file is part of Ladybug for Dyanamo
    #
    # Copyright (c) 2013-2015, Mostapha Sadeghipour Roudsari <Sadeghipour@gmail.com>
    # Ladybug is free software; you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published
    # by the Free Software Foundation; either version 3 of the License,
    # or (at your option) any later version.
    #
    # Ladybug is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    # GNU General Public License for more details.
    #
    # You should have received a copy of the GNU General Public License
    # along with Ladybug; If not, see <http://www.gnu.org/licenses/>.
    #
    # @license GPL-3.0+ <http://spdx.org/licenses/GPL-3.0+>
    """

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

    # append ladybug path to sys.path
    sys.path.append(getPackagePath('Ladybug'))

    ###### start you code from here ###

    outputsDescription = """
            location: Ladybug location
            """

    # import Ladybug libraries
    from ladybugdynamo.location import Location

    # read Dynamo inputs
    city, latitude, longitude, timeZone, elevation = IN

    # create a ladybug location
    location = Location()
    location.city = city
    location.latitude = latitude
    location.longitude = longitude
    location.timezone = timeZone
    location.elevation = elevation

    OUT = location
except Exception, e:
    OUT = "ERROR: %s" % str(e) + \
        "\nIf you think this is a bug submit an issue on github.\n" + \
        "https://github.com/ladybug-analysis-tools/ladybug-dynamo/issues"
