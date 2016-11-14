# ##### start you code from here #####
from ladybugdynamo.dt import LBDateTime

# calculate sunpath data
# get location data
dt = LBDateTime(*IN)

OUT = (
	dt.HOY,
	dt.DOY,
	dt
)
