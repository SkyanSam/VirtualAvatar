import computervision
import computergraphics
import math
import clamp

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

face_deform_y_delta = 0.0
face_deform_x_delta = 0.0

while computervision.is_window_open() and computergraphics.is_window_open():
    computervision.update()

    temp_face_deform_y = clamp.clamp(computervision.head_angle_x / 10.0, -1.0, 1.0)
    temp_face_deform_x = clamp.clamp(computervision.head_angle_y / 20.0, -1.0, 1.0)
    face_deform_y_delta = temp_face_deform_y - computergraphics.face_deform_y
    face_deform_x_delta = temp_face_deform_x - computergraphics.face_deform_x
    computergraphics.face_deform_y = temp_face_deform_y
    computergraphics.face_deform_x = temp_face_deform_x

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
