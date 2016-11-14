# import Ladybug libraries
from ladybugdynamo.epw import EPW

_epwFile = IN[0]

# create an epw object
epwData = EPW(_epwFile)
OUT = epwData.location