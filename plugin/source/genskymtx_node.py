# ##### start you code from here ###
import ladybugdynamo.sky as sky

# get input data
pluginPath = tuple(p for p in sys.path if p.endswith('Ladybug\\extra'))[0]
epwfile = IN[0]
skyDensity = IN[1]
workingDir = IN[2] if IN[2].strip() != "" else pluginPath + "\\temp\\cumulativeSkies"

cSky = sky.CumulativeSkyMtx(epwfile, skyDensity=skyDensity, workingDir=workingDir)

cSky.gendaymtx(recalculate=True,
			   pathToRadianceBinaries=pluginPath.replace("extra", "bin"))

# assign sky to output
OUT = cSky
