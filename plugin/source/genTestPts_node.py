###### start you code from here ###
import ladybugdynamo.geometryoperations as go

# Generate test points
surfaces = IN[0] if isinstance(IN[0], list) else [IN[0]]
numOfSegments = IN[1]
distanceFromBaseSrf = IN[2]
pts = []
normals = []

for srf in surfaces:
	p, n = go.generatePointsFromSurface(srf, numOfSegments, distanceFromBaseSrf)
	pts.append(p)
	normals.append(n)
OUT = pts, normals
