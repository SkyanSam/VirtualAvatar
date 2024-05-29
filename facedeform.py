import lerp
import facedeformsurface
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import texture
import mesh

face_deform_mesh = None
face_deform_x = 0.0
face_deform_y = 0.0

def generate_points(x, y):
    positions = []
    indices = []
    colors = []

    pts = facedeformsurface.evaluate(x,y)
    for y in range(8):
        for x in range(8):
            tX = float(x) / 8.0
            tY = float(y) / 8.0
            topLine = lerp.lerp3(pts[0], pts[1], pts[2], tX)
            bottomLine = lerp.lerp3(pts[3], pts[4], pts[5], tX)
            pt = lerp.lerp2(topLine, bottomLine, tY)
            positions.append(float(pt[0]))
            positions.append(float(pt[1]))
            colors.append(tX)
            colors.append(tY)

    def get_index(x, y):
        return (y * 8) + x

    for y in range(7):
        for x in range(7):
            A = get_index(x,y)
            B = get_index(x+1,y)
            C = get_index(x+1,y+1)
            D = get_index(x,y+1)
            indices.append(A)
            indices.append(C)
            indices.append(D)
            indices.append(A)
            indices.append(B)
            indices.append(C)
    
    positions = np.array(positions, dtype=np.float32)
    colors = np.array(colors, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)
    return positions, colors, indices

def start():
    global face_deform_mesh
    global left_eye_mesh
    global left_eyelid_mesh
    global left_iris_mesh
    global right_eye_mesh
    global right_eyelid_mesh
    global right_iris_mesh
    # Import Texture
    textureID = texture.read_texture("GawrGura.png")

    texture_L_eye_half = texture.read_texture("assets/L eye 0.6.png")
    texture_L_eye_full = texture.read_texture("assets/L eye 1.0.png")
    # keep going for all assets...
    # also make sure to set the min and max stuff for uv..
    # and also make sure there is a fully blank transparent png for the eye 0.0.png
    # ok cool have fun coding! YOU CAN DO THIS

    # Generate Vertexes
    positions, colors, indices = generate_points(0.0,0.0)
    # Make mesh
    face_deform_mesh = mesh.Mesh(positions, colors, indices, textureID, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")

def update():
    global face_deform_mesh
    global face_deform_x, face_deform_y
    global left_eye_openness
    global right_eye_openness
    global mouth_openness_x
    global mouth_openness_y
    global left_iris_x, left_iris_y
    global right_iris_x, right_iris_y
    # Generate Vertices
    positions, colors, indices = generate_points(face_deform_x,face_deform_y)
    # Set Position SubData, and Draw Elements
    face_deform_mesh.update_positions(positions)
    face_deform_mesh.draw()

def close():
    face_deform_mesh.delete()
