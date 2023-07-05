import computervision
import computergraphics
import math

"""
A FEW ISSUES

One: Bad rotation of face, instead I may want to consider pose estimation like this: https://www.youtube.com/watch?v=-toNMaS4SeQ&t=950s
This will handle the XY rotation but not the Z rotation (which can be handled using the angle between cartesian x axis and face x axis)

Two: The bezier surfaces don't smooth correctly, the points are likely correct but the order of those points likely is not.
Figure out a better method. My idea is to inverse either/both/none x and y coordinate depending on each quadrant and make freeform surfaces based on that 

You can do this, once this is done I will
Abstract the Triangulation texture code
Then I will work on making a bone tool
"""

computervision.start()
computergraphics.start()

while computervision.is_window_open() and computergraphics.is_window_open():
    computervision.update()

    computergraphics.face_deform_y = computervision.face_x_angle / 20.0
    if computergraphics.face_deform_y < -1.0: computergraphics.face_deform_x = -1.0
    elif computergraphics.face_deform_y > 1.0: computergraphics.face_deform_x = 1.0

    computergraphics.update()
    
computervision.end()
computergraphics.end()

"""

import computergraphics

computergraphics.start()

while computergraphics.is_window_open():
    computergraphics.update()

computergraphics.end()
"""
