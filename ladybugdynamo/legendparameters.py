from ladybug.legendparameters import *
import color

class LegendParameters(LBLegendParameters):
    """Ladybug lagend parameters

        Attributes:
            legendRange: Input a list of numbers or strings to set the boundary of legend. The default is ['min', 'max']
            numberOfSegments: An interger representing the number of steps between the high and low boundary of the legend.
                    The default is set to 11 and any custom values put in here should always be greater than or equal to 2.
            colors: An optional list of colors. Default is Ladybug's default colorset
            chartType: 0: continuous, 1: segmented, 2: ordinal. Default: 0. Ordinal values can be strings and well as numericals
            title:  Legend title. It's usually analysis unit
            font: An optional text string that sets the font of the text. Examples include "Arial", "Times New Roman" or "Courier" (all without quotations). The text input here can be any font that is on your computer but the font must be of an Editable file type (as seen in the font folder off of your control panel).  Font files that are Print and Preview will not work.  If you wish to use a Bold version of the font, include a ", Bold" at the end of the font name (example: "Arial, Bold").
            fontSize: An optional number to set the size of the text in model's units.
            scale: Input a number here to change the scale of the legend. The default is set to 1.
            basePlane: Input a plane to change the location and orientation of the legend. The default is set to the right of the analysis scene in XY plane.
            vertical: Set to False to get a horizontal legend. Default is vertical.

        Usage:
            lp = LBLegendParameters(legendRange = [2, 28])
            print lp.color(10)

    """
    # TODO: Add textual and geometry parts
    def __init__(self, legendRange = ['min', 'max'], numberOfSegments = 11, colors = None, \
        chartType = 0):
        LBLegendParameters.__init__(self, legendRange, numberOfSegments, colors, chartType)

    def calculateColor(self, value):
        "Return color for a specific value"
        return color.ColorConvertor.toDSColor(self.colorRange.color(value)).next()

    @property
    def colors(self):
        "Return color for a specific value"
        return color.ColorConvertor.toDSColor(self.colorRange.colors)

    def geometry(self):
        raise NotImplementedError()

    def text(self):
        raise NotImplementedError()
