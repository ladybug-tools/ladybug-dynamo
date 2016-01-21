"""
# import .epw file
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
    #Get path to dynamo package using the package name
    dynamoPath = clr.References[2].Location.split('\\')[2].replace(' ', '\\')
    appdata = os.getenv('APPDATA')
    return '%s\%s\packages\%s\extra\\'%(appdata, dynamoPath, packageName)

# append ladybug path to sys.path
sys.path.append(getPackagePath('Ladybug'))

###### start you code from here ###
outputsDescription = """
        location: A list of text summarizing the location data in the weather file (use this to construct the sun path).

        dryBulbTemperature: "This is the houlry dry bulb temperature, in C. Note that this is a full numeric field (i.e. 23.6) and not an integer representation with tenths. Valid values range from 70 C to 70 C. Missing value for this field is 99.9."

        dewPointTemperature: "This is the hourly dew point temperature, in C. Note that this is a full numeric field (i.e. 23.6) and not an integer representation with tenths. Valid values range from 70 C to 70 C. Missing value for this field is 99.9."

        relativeHumidity: "This is the hourly Relative Humidity in percent. Valid values range from 0% to 110%. Missing value for this field is 999."

        windDirection: "This is the hourly Wind Direction in degrees where the convention is that North=0.0, East=90.0, South=180.0, West=270.0. (If wind is calm for the given hour, the direction equals zero.) Values can range from 0 to 360. Missing value is 999."

        windSpeed: "This is the hourly wind speed in m/sec. Values can range from 0 to 40. Missing value is 999."

        directNormalRadiation: "This is the hourly Direct Normal Radiation in Wh/m2. (Amount of solar radiation in Wh/m2 received directly from the solar disk on a surface perpendicular to the sun's rays, during the number of minutes preceding the time indicated.) If the field is missing ( 9999) or invalid (<0), it is set to 0. Counts of such missing values are totaled and presented at the end of the runperiod."

        diffuseHorizontalRadiation: "This is the hourly Diffuse Horizontal Radiation in Wh/m2. (Amount of solar radiation in Wh/m2 received from the sky (excluding the solar disk) on a horizontal surface during the number of minutes preceding the time indicated.) If the field is missing ( 9999) or invalid (<0), it is set to 0. Counts of such missing values are totaled and presented at the end of the runperiod."

        globalHorizontalRadiation: "This is the hourly Global Horizontal Radiation in Wh/m2. (Total amount of direct and diffuse solar radiation in Wh/m2 received on a horizontal surface during the number of minutes preceding the time indicated.) It is not currently used in EnergyPlus calculations. It should have a minimum value of 0; missing value for this field is 9999."

        directNormalIlluminance: "This is the hourly Direct Normal Illuminance in lux. (Average amount of illuminance in hundreds of lux received directly from the solar disk on a surface perpendicular to the sun's rays, during the number of minutes preceding the time indicated.) It is not currently used in EnergyPlus calculations. It should have a minimum value of 0; missing value for this field is 999999 and will be considered missing of >= 999900."

        diffuseHorizontalIlluminance: "This is the hourly Diffuse Horizontal Illuminance in lux. (Average amount of illuminance in hundreds of lux received from the sky (excluding the solar disk) on a horizontal surface during the number of minutes preceding the time indicated.) It is not currently used in EnergyPlus calculations. It should have a minimum value of 0; missing value for this field is 999999 and will be considered missing of >= 999900."

        globalHorizontalIlluminance: "This is the hourly Global Horizontal Illuminance in lux. (Average total amount of direct and diffuse illuminance in hundreds of lux received on a horizontal surface during the number of minutes preceding the time indicated.) It is not currently used in EnergyPlus calculations. It should have a minimum value of 0; missing value for this field is 999999 and will be considered missing of >= 999900."

        totalSkyCover: "This is the fraction for total sky cover (tenths of coverage). (i.e. 1 is 1/10 covered. 10 is total coverage). (Amount of sky dome in tenths covered by clouds or obscuring phenomena at the hour indicated at the time indicated.) Minimum value is 0; maximum value is 10; missing value is 99."

        liquidPrecipitationDepth: "The amount of liquid precipitation(mm) observed at the indicated hour for the period indicated in the liquid precipitation quantity field. If this value is not missing, then it is used and overrides the precipitation flag as rainfall.  Conversely, if the precipitation flag shows rain and this field is missing or zero, it is set to 1.5 (mm)."

        barometricPressure: "This is the hourly weather station pressure in Pa. Valid values range from 31,000 to 120,000... Missing value for this field is 999999."

        modelYear: The year from which the hourly data has been extracted. EPW files are synthesized from real recorded data from different years in a given climate. This is done to ensure that, for each month, the selected data is statistically representative of the average monthly conditions over the 18+ years of recording the data. Different EPW files will be synthesized from different years depeding on whether they are TMY (Typical Meteorological Year), TMY2, TMY3, AMY (Actual Meteorological Year) or other.
        """

# import Ladybug libraries
import ladybugdynamo.epw as epw
import ladybugdynamo.core as core

# assign inputs from dynamo python node
_epwFile, _analysisPeriod_ = IN
#_epwFile, _analysisPeriod_ = 'C:\EnergyPlusV8-3-0\WeatherData\USA_CA_San.Francisco.Intl.AP.724940_TMY3.epw', '10/1 to 12/31 between 1 to 24'
# create an epw object
epwData = epw.EPW(_epwFile)
analysisPeriod = core.AnalysisPeriod.fromAnalysisPeriod(_analysisPeriod_)

OUT = [
        epwData.location,
        epwData.dryBulbTemperature.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.dewPointTemperature.filterByAnalysisPeriod(analysisPeriod).values(header = True),
		epwData.relativeHumidity.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.windDirection.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.windSpeed.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.directNormalRadiation.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.diffuseHorizontalRadiation.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.globalHorizontalRadiation.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.directNormalIlluminance.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.diffuseHorizontalIlluminance.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.globalHorizontalIlluminance.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.totalSkyCover.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.liquidPrecipitationDepth.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.atmosphericStationPressure.filterByAnalysisPeriod(analysisPeriod).values(header = True),
        epwData.years.filterByAnalysisPeriod(analysisPeriod).values(header = True)
        ]
