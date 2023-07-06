from geomdl import knotvector
from geomdl import BSpline
from geomdl import utilities
import time
import copy
import clamp

ptsC = [
[-.5,.5],
[.0,.5],
[.5,.5],
[-.5,-.5],
[.0,-.5],
[.5,-.5]
]

ptsR = [
[-.4,.4],
[.1,.5],
[.6,.6],
[-.4,-.6],
[.1,-.5],
[.6,-.4]
]

ptsL = [
[-.6,.6],
[-.1,.5],
[.4,.4],
[-.6,-.4],
[-.1,-.5],
[.4,-.6]
]

ptsU = [
[-.4,.6],
[-.0,.6],
[.4,.6],
[-.6,-.4],
[-.0,-.2],
[.6,-.4]
]

ptsD = [
[-.6,.4],
[-.0,.2],
[.6,.4],
[-.4,-.6],
[-.0,-.6],
[.4,-.6]
]

ptsDR = [
[-.5,.3],
[.2,.1],
[.7,.5],
[-.3,-.7],
[.1,-.6],
[.4,-.5]
]

ptsDL = [
[-.7,.5],
[-.2,.1],
[.5,.3],
[-.5,-.5],
[-.1,-.6],
[.3,-.7]
]

ptsUL = [
[-.5,.7],
[-.1,.6],
[.3,.5],
[-.7,-.3],
[.2,-.1],
[.5,-.5]
]

ptsUR = [
[-.3,.5],
[.1,.6],
[.5,.7],
[-.5,-.5],
[-.2,-.1],
[.7,-.5]
]

surfacesQI = []
surfacesQII = []
surfacesQIII = []
surfacesQIV = []

surf = BSpline.Surface()
surf.degree_u = 1
surf.degree_v = 1
surf.ctrlpts2d = [
    [[-1, -1], [-1, 1]],
    [[1, -1], [1, 1]]
]
surf.knotvector_u = utilities.generate_knot_vector(1, 2, knotvector_type="uniform")
surf.knotvector_v = utilities.generate_knot_vector(1, 2, knotvector_type="uniform")
print(surf.knotvector_u)
print(surf.knotvector_v)
surf.delta = 0.025

for i in range(6):
    surfQI = copy.deepcopy(surf)
    surfQII = copy.deepcopy(surf)
    surfQIII = copy.deepcopy(surf)
    surfQIV = copy.deepcopy(surf)

    # Note surfaces are flipped on the y axis
    surfQI.ctrlpts2d = [
        [ptsC[i], ptsR[i]],
        [ptsU[i], ptsUR[i]]
    ]
    surfQII.ctrlpts2d = [
        [ptsC[i], ptsL[i]],
        [ptsU[i], ptsUL[i]]
    ]
    surfQIII.ctrlpts2d = [
        [ptsC[i], ptsL[i]],
        [ptsD[i], ptsDL[i]],
        
    ]
    surfQIV.ctrlpts2d = [
        [ptsC[i], ptsR[i]],
        [ptsD[i], ptsDR[i]],
    ]
    

    surfacesQI.append(surfQI)
    surfacesQII.append(surfQII)
    surfacesQIII.append(surfQIII)
    surfacesQIV.append(surfQIV)

# Input is any x and y value between -1.0 and 1.0
def evaluate(x, y):
    x = clamp.clamp(x, -1.0, 1.0)
    y = clamp.clamp(y, -1.0, 1.0)
    pts = []
    if 0 <= x and 0 <= y:
        for surf in surfacesQI:
            pts.append(surf.evaluate_single((y,x)))
    elif x <= 0 and 0 <= y:
        for surf in surfacesQII:
            pts.append(surf.evaluate_single((y,-x)))
    elif x <= 0 and y <= 0:
        for surf in surfacesQIII:
            pts.append(surf.evaluate_single((-y,-x)))
    elif 0 <= x and y <= 0:
        for surf in surfacesQIV:
            pts.append(surf.evaluate_single((-y,x)))
    return pts

assert evaluate(0.0,0.0) == ptsC
assert evaluate(1.0,0.0) == ptsR
assert evaluate(1.0,1.0) == ptsUR
assert evaluate(0.0,1.0) == ptsU
assert evaluate(-1.0,1.0) == ptsUL
assert evaluate(-1.0,0.0) == ptsL
assert evaluate(-1.0,-1.0) == ptsDL
assert evaluate(0.0,-1.0) == ptsD
assert evaluate(1.0,-1.0) == ptsDR