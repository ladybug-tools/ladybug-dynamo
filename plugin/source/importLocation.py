"""
# Import location
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
        location: Ladybug location
        """

# import Ladybug libraries
import ladybugdynamo.epw as epw

_epwFile = IN[0]
#_epwFile, _analysisPeriod_ = 'C:\EnergyPlusV8-3-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw', '10/1 to 12/31 between 1 to 24'
# create an epw object
epwData = epw.EPW(_epwFile)
OUT = epwData.location
