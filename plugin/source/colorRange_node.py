# ##### start you code from here ###
import ladybugdynamo.color as color

index = IN[0]
cs = color.LBColorset()
colors = cs[index]
OUT = color.ColorConvertor.toDSColor(colors)