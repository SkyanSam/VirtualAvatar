from geomdl import knotvector
from geomdl import BSpline
from geomdl import utilities

surf = BSpline.Surface()

surf.degree_u = 1
surf.degree_v = 1

surf.ctrlpts2d = [
    [[-1, -1], [-1, 1]],
    [[1, -1], [1, 1]]
]

#surf.knotvector_u = [0.0,0.0,0.0,0.33,0.66,1.0,1.0,1.0] 
#surf.knotvector_v = [0.0,0.0,0.0,0.33,0.66,1.0,1.0,1.0]

surf.knotvector_u = utilities.generate_knot_vector(1, 2, knotvector_type="uniform")
surf.knotvector_v = utilities.generate_knot_vector(1, 2, knotvector_type="uniform")

surf.delta = 0.025

print(surf.evaluate_single((0.33,0.77)))

# Now make one for each point
# There are nine possible configs for each point
# There are 8 points if we do 3 degree bezier, and 6 points if we do 2 degree
# See if 2 degree can represent and if so use it (less work, more centered too)


# We need 4 different bezier surfaces for each quadrant there you go