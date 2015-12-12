"""
# Deconstruct location
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

# Now that the path to IronPython is stablished we can import libraries
import os
import clr
clr.AddReference('DynamoCore')

def getPackagePath(packageName):
    """Get path to dynamo package using the package name"""
    dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
    appdata = os.getenv('APPDATA')
    return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

# append ladybug path to sys.path
sys.path.append(getPackagePath('Ladybug'))

###### start you code from here ###

outputsDescription = """
        locationName: Name of the location.
        latitude: Latitude of the location.
        longitude: Longitude of the location.
        timeZone: Time zone of the location.
        elevation: Elevation of the location.
        """

# import Ladybug libraries
import ladybugdynamo.core as core

# create a ladybug location
location = core.Location()
location.createFromEPString(str(IN[0]))

OUT = [
    location.city,
    location.latitude,
    location.longitude,
    location.timeZone,
    location.elevation
    ]
