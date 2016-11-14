# ##### start you code from here ###
# get input data
# unwrap sky
cSky = IN[0]

# instance check fails!
# assert isinstance(cSky, CumulativeSkyMtx), "Input sky is not a LBCumulativeSky"
assert type(cSky).__name__ == "CumulativeSkyMtx", "Input sky is not a LBCumulativeSky"

# get hours of the year
HOYs = IN[1] if isinstance(IN[1], list) else [IN[1]]
includeDiffuse = IN[2]
includeDirect = IN[3]

cSky.gendaymtx(diffuse=includeDiffuse, direct=includeDirect,
			   analysisPeriod=HOYs)

# Assign your output to the OUT variable.
OUT = (cSky,
	   (cSky.skyTotalRadiation.values(header=True),
		cSky.skyDiffuseRadiation.values(header=True),
		cSky.skyDirectRadiation.values(header=True))
	   )