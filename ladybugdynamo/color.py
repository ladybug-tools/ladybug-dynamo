from ladybug.color import LBColor, LBColorset, LBColorRange

# import Dynamo libraries
import clr
clr.AddReference("DSCoreNodes")
from DSCore import Color as DSColor


class ColorConvertor(object):
    """Color convertor.

    This class converts ladybug colors to Dynamo colors.
    """

    @staticmethod
    def toDSColor(ladybugColors):
        """Convert a LBColor into Dynamo color."""
        if hasattr(ladybugColors, "__iter__"):

            for col in ladybugColors:
                assert isinstance(col, LBColor), \
                    "%s in not an instance of LBColor" % str(col)

                yield DSColor.ByARGB(255, col.r, col.g, col.b)
        else:
            assert isinstance(ladybugColors, LBColor), \
                "%s in not an instance of LBColor" % str(ladybugColors)

            yield DSColor.ByARGB(255, ladybugColors.r, ladybugColors.g, ladybugColors.b)

    @staticmethod
    def toLBColor(DSColors):
        """Convert a Dynamo color or a list of Dynamo colors to ladybug colors."""
        if hasattr(DSColors, "__iter__"):

            for col in DSColors:
                assert isinstance(col, DSColor), \
                    "%s in not an instance of DSColor" % str(col)

                yield LBColor(col.Red, col.Green, col.Blue)
        else:
            assert isinstance(DSColors, DSColor), \
                "%s in not an instance of DSColor" % str(DSColors)

            yield LBColor(DSColors.Red, DSColors.Green, DSColors.Blue)
