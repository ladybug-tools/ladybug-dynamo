# assign inputs
_epwFile = IN[0]
location = dryBulbTemperature = dewPointTemperature = relativeHumidity = windSpeed = windDirection = directNormalRadiation = diffuseHorizontalRadiation = globalHorizontalRadiation = directNormalIlluminance = diffuseHorizontalIlluminance = globalHorizontalIlluminance = totalSkyCover = liquidPrecipitationDepth = barometricPressure = modelYear = None

try:
    import ladybug.epw as epw
    import ladybug.output as output
except ImportError:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _epwFile:
    epwData = epw.EPW(_epwFile)
    location = epwData.location
    dryBulbTemperature = output.wrap(epwData.dryBulbTemperature.values)
    dewPointTemperature = output.wrap(epwData.dewPointTemperature.values)
    relativeHumidity = output.wrap(epwData.relativeHumidity.values)
    windDirection = output.wrap(epwData.windDirection.values)
    windSpeed = output.wrap(epwData.windSpeed.values)
    directNormalRadiation = output.wrap(epwData.directNormalRadiation.values)
    diffuseHorizontalRadiation = output.wrap(epwData.diffuseHorizontalRadiation.values)
    globalHorizontalRadiation = output.wrap(epwData.globalHorizontalRadiation.values)
    directNormalIlluminance = output.wrap(epwData.directNormalIlluminance.values)
    diffuseHorizontalIlluminance = output.wrap(epwData.diffuseHorizontalIlluminance.values)
    globalHorizontalIlluminance = output.wrap(epwData.globalHorizontalIlluminance.values)
    totalSkyCover = output.wrap(epwData.totalSkyCover.values)
    liquidPrecipitationDepth = output.wrap(epwData.liquidPrecipitationDepth.values)
    barometricPressure = output.wrap(epwData.atmosphericStationPressure.values)
    modelYear = output.wrap(epwData.years.values)

# assign outputs to OUT
OUT = location, dryBulbTemperature, dewPointTemperature, relativeHumidity, windSpeed, windDirection, directNormalRadiation, diffuseHorizontalRadiation, globalHorizontalRadiation, directNormalIlluminance, diffuseHorizontalIlluminance, globalHorizontalIlluminance, totalSkyCover, liquidPrecipitationDepth, barometricPressure, modelYear