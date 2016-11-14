###### start you code from here ###
import ladybugdynamo.legendparameters as legendpar

# analysis surfaces will be useful for drawing the legend. No use for now.
values = IN[0]
legendPar = IN[1] if IN[1] else legendpar.LegendParameters()
OUT = legendPar.calculateColors(values)
