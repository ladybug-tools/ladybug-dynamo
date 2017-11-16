# assign inputs
_epwFile = IN[0]
location = dryBulbTemperature = dewPointTemperature = relativeHumidity = windSpeed = windDirection = directNormalRadiation = diffuseHorizontalRadiation = globalHorizontalRadiation = directNormalIlluminance = diffuseHorizontalIlluminance = globalHorizontalIlluminance = totalSkyCover = liquidPrecipitationDepth = barometricPressure = modelYear = None

try:
    import ladybug.epw as epw
    import ladybug.output as output
except ImportError:
    raise ImportError('\nFailed to import ladybug:\n\t{}'.format(e))

if _epwFile:
    epw_data = epw.EPW(_epwFile)
    location = epw_data.location
    dryBulbTemperature = output.wrap(epw_data.dry_bulb_temperature.values)
    dewPointTemperature = output.wrap(epw_data.dew_point_temperature.values)
    relativeHumidity = output.wrap(epw_data.relative_humidity.values)
    windDirection = output.wrap(epw_data.wind_direction.values)
    windSpeed = output.wrap(epw_data.wind_speed.values)
    directNormalRadiation = output.wrap(epw_data.direct_normal_radiation.values)
    diffuseHorizontalRadiation = output.wrap(epw_data.diffuse_horizontal_radiation.values)
    globalHorizontalRadiation = output.wrap(epw_data.global_horizontal_radiation.values)
    directNormalIlluminance = output.wrap(epw_data.direct_normal_illuminance.values)
    diffuseHorizontalIlluminance = output.wrap(epw_data.diffuse_horizontal_illuminance.values)
    globalHorizontalIlluminance = output.wrap(epw_data.global_horizontal_illuminance.values)
    totalSkyCover = output.wrap(epw_data.total_sky_cover.values)
    liquidPrecipitationDepth = output.wrap(epw_data.liquid_precipitation_depth.values)
    barometricPressure = output.wrap(epw_data.atmospheric_station_pressure.values)
    modelYear = output.wrap(epw_data.years.values)

# assign outputs to OUT
OUT = location, dryBulbTemperature, dewPointTemperature, relativeHumidity, windSpeed, windDirection, directNormalRadiation, diffuseHorizontalRadiation, globalHorizontalRadiation, directNormalIlluminance, diffuseHorizontalIlluminance, globalHorizontalIlluminance, totalSkyCover, liquidPrecipitationDepth, barometricPressure, modelYear