def getDynamoPath():
	return os.path.split(clr.References[2].Location)[0]

	sys.path.append(getDynamoPath())  # This is for using colors

###### start you code from here ###
import ladybugdynamo.legendparameters as legendpar
from ladybugdynamo.color import ColorConvertor

chartType = IN[0]
legendRange = IN[1] if IN[1]!=[] else ['min', 'max']
colors = list(ColorConvertor.toLBColor(IN[2]))

OUT = legendpar.LegendParameters(legendRange=legendRange,
								 numberOfSegments=11,
								 colors=colors,
								 chartType=chartType)

