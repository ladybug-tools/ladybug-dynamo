###### start you code from here ###
import ladybugdynamo.sunlighthours as sunlighthours


# get input data
testPoints = IN[0] if isinstance(IN[0], list) else [IN[0]]
geometries = IN[1] if isinstance(IN[1], list) else [IN[1]]
sunVectors = IN[2] if isinstance(IN[2], list) else [IN[2]]

# TODO: Integrate datetime into analysis
slh = sunlighthours.Sunlighthours(sunVectors, [], testPoints, geometries)
slh.runAnalysis()

# assign outputs
OUT = slh.results
del(slh)
