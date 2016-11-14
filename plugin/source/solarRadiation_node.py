###### start you code from here ###
import ladybugdynamo.solarradiation as radiation

# get input data
testPoints = IN[0] if isinstance(IN[0], list) else [IN[0]]
pointsNormal = IN[1] if isinstance(IN[1], list) else [IN[1]]
geometries = IN[2] if isinstance(IN[2], list) else [IN[2]]
sky = IN[3]

assert type(sky).__name__ == "CumulativeSkyMtx", "Input sky is not a LBCumulativeSky"

# TODO: Integrate datetime into analysis
radAnalysis = radiation.SolarRadiation(sky, testPoints, pointsNormal, geometries)
radAnalysis.runAnalysis()

# assign outputs
OUT = radAnalysis.results
del(radAnalysis)
