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
    
    # Import Texture
    textureID = texture.read_texture("GawrGura.png")

    global texture_empty
    global texture_L_eye_06
    global texture_L_eye_10
    global texture_L_eyelid_00
    global texture_L_eyelid_06
    global texture_L_eyelid_10
    global texture_L_pupil
    global texture_R_eye_06
    global texture_R_eye_10
    global texture_R_eyelid_00
    global texture_R_eyelid_06
    global texture_R_eyelid_10
    global texture_R_pupil
    global uv_start
    global uv_end

    texture_empty = texture.read_texture("assets/empty.png")
    texture_L_eye_06 = texture.read_texture("assets/L eye 0.6.png")
    texture_L_eye_10 = texture.read_texture("assets/L eye 1.0.png")
    texture_L_eyelid_00 = texture.read_texture("assets/L eyelid 0.0.png")
    texture_L_eyelid_06 = texture.read_texture("assets/L eyelid 0.6.png")
    texture_L_eyelid_10 = texture.read_texture("assets/L_eyelid 1.0.png")
    texture_L_pupil = texture.read_texture("assets/L pupil.png")
    texture_R_eye_06 = texture.read_texture("assets/R eye 0.6.png")
    texture_R_eye_10 = texture.read_texture("assets/R eye 1.0.png")
    texture_R_eyelid_00 = texture.read_texture("assets/R eyelid 0.0.png")
    texture_R_eyelid_06 = texture.read_texture("assets/R eyelid 0.6.png")
    texture_R_eyelid_10 = texture.read_texture("assets/R_eyelid 1.0.png")
    texture_R_pupil = texture.read_texture("assets/R pupil.png")

    # Generate Vertexes
    positions, colors, indices = generate_points(0.0,0.0)
    # Make mesh
    uv_start = np.array([0.0,0.0])
    uv_end = np.array([1.0,1.0])

    global L_pupil_mesh
    global L_eyelid_mesh
    global L_eye_mesh
    global R_pupil_mesh
    global R_eyelid_mesh
    global R_eye_mesh

    L_pupil_mesh = mesh.Mesh(positions, colors, indices, texture_L_pupil, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")
    L_eyelid_mesh = mesh.Mesh(positions, colors, indices, texture_L_eyelid_10, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")
    L_eye_mesh = mesh.Mesh(positions, colors, indices, texture_L_eye_10, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")
    R_pupil_mesh = mesh.Mesh(positions, colors, indices, texture_R_pupil, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")
    R_eyelid_mesh = mesh.Mesh(positions, colors, indices, texture_R_eyelid_10, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")
    R_eye_mesh = mesh.Mesh(positions, colors, indices, texture_R_eye_10, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")
    face_deform_mesh = mesh.Mesh(positions, colors, indices, textureID, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")


def get_texture_id(openness, tex_00, tex_06, tex_10):
    r_tex = tex_00 if openness > 0.0 else r_tex
    r_tex = tex_06 if openness > 0.6 else r_tex
    r_tex = tex_10 if openness > 1.0 else r_tex
    return r_tex

def update():
    iris_uv_offset = 0.1

    global face_deform_mesh
    global face_deform_x, face_deform_y
    global left_eye_open
    global right_eye_open
    global mouth_open_x
    global mouth_open_y
    global left_iris_x, left_iris_y
    global right_iris_x, right_iris_y
    # Generate Vertices
    positions, colors, indices = generate_points(face_deform_x,face_deform_y)
    
    # Set Correct Texture Based on Eye Openness
    L_eye_mesh.textureID = get_texture_id(left_eye_open, texture_empty, texture_L_eye_06, texture_L_eye_10)
    L_eyelid_mesh.textureID = get_texture_id(left_eye_open, texture_L_eyelid_00, texture_L_eyelid_06, texture_L_eyelid_10)
    R_eye_mesh.textureID = get_texture_id(right_eye_open, texture_empty, texture_R_eye_06, texture_R_eye_10)
    R_eyelid_mesh.textureID = get_texture_id(right_eye_open, texture_R_eyelid_00, texture_R_eyelid_06, texture_R_eyelid_10)
    
    # Iris Movement
    L_pupil_mesh.uv_start = uv_start + np.array([left_iris_x * iris_uv_offset, left_iris_y * iris_uv_offset])
    L_pupil_mesh.uv_end = uv_end + np.array([left_iris_x * iris_uv_offset, left_iris_y * iris_uv_offset])
    R_pupil_mesh.uv_start = uv_start + np.array([right_iris_x * iris_uv_offset, right_iris_y * iris_uv_offset])
    R_pupil_mesh.uv_end = uv_end + np.array([right_iris_x * iris_uv_offset, right_iris_y * iris_uv_offset])

    # Set Position SubData, and Draw Elements
    facemeshes = [L_pupil_mesh, L_eyelid_mesh, L_eye_mesh, R_pupil_mesh, R_eyelid_mesh, R_eye_mesh, face_deform_mesh] # note may want to adjust draw order..
    for m in facemeshes:
        m.update_positions(positions)
        m.draw()

def close():
    face_deform_mesh.delete()
