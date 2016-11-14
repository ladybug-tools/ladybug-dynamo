# import Ladybug libraries
from ladybugdynamo.epw import EPW
from ladybugdynamo.analysisperiod import AnalysisPeriod

# assign inputs from dynamo python node
_epwFile, _analysisPeriod_ = IN

# create an epw object
epwData = EPW(_epwFile)
analysisPeriod = AnalysisPeriod.fromAnalysisPeriod(_analysisPeriod_)

OUT = [
	epwData.location,
	epwData.dryBulbTemperature.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.dewPointTemperature.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.relativeHumidity.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.windDirection.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.windSpeed.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.directNormalRadiation.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.diffuseHorizontalRadiation.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.globalHorizontalRadiation.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.directNormalIlluminance.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.diffuseHorizontalIlluminance.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.globalHorizontalIlluminance.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.totalSkyCover.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.liquidPrecipitationDepth.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.atmosphericStationPressure.filterByAnalysisPeriod(analysisPeriod).values(header=True),
	epwData.years.filterByAnalysisPeriod(analysisPeriod).values(header=True)
]
