import lerp
import facedeformsurface
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import texture
import mesh
from collections import namedtuple

face_deform_mesh = None
face_deform_x = 0.0
face_deform_y = 0.0
face_expression_data = None

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

def create_face_deform_mesh(textureID, arr):
    return mesh.Mesh(arr[0], arr[1], arr[2], textureID, arr[3], arr[4], "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")

def start():
    global face_deform_mesh
    
    # Import Texture
    #textureID = texture.read_texture("GawrGura.png")

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
    global texture_mouth_00_neg_10
    global texture_mouth_00_00
    global texture_mouth_00_10
    global texture_mouth_03_neg_10
    global texture_mouth_03_00
    global texture_mouth_03_10
    global texture_mouth_10_neg_10
    global texture_mouth_10_00
    global texture_mouth_10_10
    global uv_start
    global uv_end

    texture_empty = texture.read_texture("assets/empty.png")
    texture_L_eye_06 = texture.read_texture("assets/L eye 0.6.png")
    texture_L_eye_10 = texture.read_texture("assets/L eye 1.0.png")
    texture_L_eyelid_00 = texture.read_texture("assets/L eyelid 0.0.png")
    texture_L_eyelid_06 = texture.read_texture("assets/L eyelid 0.6.png")
    texture_L_eyelid_10 = texture.read_texture("assets/L eyelid 1.0.png")
    texture_L_pupil = texture.read_texture("assets/L pupil.png")
    texture_R_eye_06 = texture.read_texture("assets/R eye 0.6.png")
    texture_R_eye_10 = texture.read_texture("assets/R eye 1.0.png")
    texture_R_eyelid_00 = texture.read_texture("assets/R eyelid 0.0.png")
    texture_R_eyelid_06 = texture.read_texture("assets/R eyelid 0.6.png")
    texture_R_eyelid_10 = texture.read_texture("assets/R eyelid 1.0.png")
    texture_R_pupil = texture.read_texture("assets/R pupil.png")
    texture_mouth_00_neg_10 = texture.read_texture("assets/mouth 0.0 & -1.0.png")
    texture_mouth_00_00 = texture.read_texture("assets/mouth 0.0 & 0.0.png")
    texture_mouth_00_10 = texture.read_texture("assets/mouth 0.0 & 1.0.png")
    texture_mouth_03_neg_10 = texture.read_texture("assets/mouth 0.3 & -1.0.png")
    texture_mouth_03_00 = texture.read_texture("assets/mouth 0.3 & 0.0.png")
    texture_mouth_03_10 = texture.read_texture("assets/mouth 0.3 & 1.0.png")
    texture_mouth_10_neg_10 = texture.read_texture("assets/mouth 1.0 & -1.0.png")
    texture_mouth_10_00 = texture.read_texture("assets/mouth 1.0 & 0.0.png")
    texture_mouth_10_10 = texture.read_texture("assets/mouth 1.0 & 1.0.png")
    texture_L_ear = texture.read_texture("assets/L antenna.png")
    texture_R_ear = texture.read_texture("assets/R ear.png")
    texture_nose = texture.read_texture("assets/nose lol.png")
    texture_head = texture.read_texture("assets/head.png")
    texture_back_hair_1 = texture.read_texture("assets/back hair 1.png")
    texture_back_hair_2 = texture.read_texture("assets/back hair 2.png")
    texture_front_hair = texture.read_texture("assets/front hair.png")


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
    global mouth_mesh
    global back_hair_1_mesh
    global back_hair_2_mesh
    global front_hair_mesh
    global head_mesh
    global L_ear_mesh
    global R_ear_mesh
    global nose_mesh

    
    #MeshCreationArrays = namedtuple('positions','colors','indices','uv_start','uv_end')
    mesh_creation_arr = [positions, colors, indices, uv_start, uv_end]
    #print(mesh_creation_arr)
    L_pupil_mesh = create_face_deform_mesh(texture_L_pupil, mesh_creation_arr)
    L_eyelid_mesh = create_face_deform_mesh(texture_L_eyelid_10, mesh_creation_arr)
    L_eye_mesh = create_face_deform_mesh(texture_L_eye_10, mesh_creation_arr)
    R_pupil_mesh = create_face_deform_mesh(texture_R_pupil, mesh_creation_arr)
    R_eyelid_mesh = create_face_deform_mesh(texture_R_eyelid_10, mesh_creation_arr)
    R_eye_mesh = create_face_deform_mesh(texture_R_eye_10, mesh_creation_arr)
    mouth_mesh = create_face_deform_mesh(texture_mouth_10_00, mesh_creation_arr)
    back_hair_1_mesh = create_face_deform_mesh(texture_back_hair_1, mesh_creation_arr)
    back_hair_2_mesh = create_face_deform_mesh(texture_back_hair_2, mesh_creation_arr)
    front_hair_mesh = create_face_deform_mesh(texture_front_hair, mesh_creation_arr)
    L_ear_mesh = create_face_deform_mesh(texture_L_ear, mesh_creation_arr)
    R_ear_mesh = create_face_deform_mesh(texture_R_ear, mesh_creation_arr)
    head_mesh = create_face_deform_mesh(texture_head, mesh_creation_arr)
    nose_mesh = create_face_deform_mesh(texture_nose, mesh_creation_arr)
    #face_deform_mesh = mesh.Mesh(positions, colors, indices, textureID, uv_start, uv_end, "shaders/facedeformv.glsl", "shaders/facedeformf.glsl")


def get_texture_id(openness, tex_00, tex_06, tex_10):
    r_tex = tex_00 
    r_tex = tex_06 if openness > 0.6 else r_tex
    r_tex = tex_10 if openness > 1.0 else r_tex
    return r_tex

def get_texture_mouth_id(open_x, open_y, tex_arr_2d):
    x_index = 2
    y_index = 2
    if (open_x < 1.55): x_index = 1
    if (open_x < 1.2): x_index = 0
    if (open_y > 0.5): y_index = 1
    if (open_y > 1.0): y_index = 0
    return tex_arr_2d[y_index][x_index]

def update():
    iris_uv_offset = 0.005

    #global face_deform_mesh
    global face_deform_x, face_deform_y
    global face_expression_data

    global texture_mouth_00_neg_10
    global texture_mouth_00_00
    global texture_mouth_00_10
    global texture_mouth_03_neg_10
    global texture_mouth_03_00
    global texture_mouth_03_10
    global texture_mouth_10_neg_10
    global texture_mouth_10_00
    global texture_mouth_10_10

    # Generate Vertices
    positions, colors, indices = generate_points(face_deform_x,face_deform_y)
    
    # Set Correct Texture Based on Eye Openness
    L_eye_mesh.textureID = get_texture_id(face_expression_data.left_eye_open, texture_empty, texture_L_eye_06, texture_L_eye_10)
    L_eyelid_mesh.textureID = get_texture_id(face_expression_data.left_eye_open, texture_L_eyelid_00, texture_L_eyelid_06, texture_L_eyelid_10)
    R_eye_mesh.textureID = get_texture_id(face_expression_data.right_eye_open, texture_empty, texture_R_eye_06, texture_R_eye_10)
    R_eyelid_mesh.textureID = get_texture_id(face_expression_data.right_eye_open, texture_R_eyelid_00, texture_R_eyelid_06, texture_R_eyelid_10)
    
    # Iris Movement
    L_pupil_mesh.uv_start = uv_start + np.array([face_expression_data.left_iris_x * iris_uv_offset, face_expression_data.left_iris_y * iris_uv_offset])
    L_pupil_mesh.uv_end = uv_end + np.array([face_expression_data.left_iris_x * iris_uv_offset, face_expression_data.left_iris_y * iris_uv_offset])
    R_pupil_mesh.uv_start = uv_start + np.array([face_expression_data.right_iris_x * iris_uv_offset, face_expression_data.right_iris_y * iris_uv_offset])
    R_pupil_mesh.uv_end = uv_end + np.array([face_expression_data.right_iris_x * iris_uv_offset, face_expression_data.right_iris_y * iris_uv_offset])

    # Set Correct Texture Based on Mouth Openness
    mouth_mesh.textureID = get_texture_mouth_id(
        face_expression_data.mouth_open_x, face_expression_data.mouth_open_y,
        [
            [texture_mouth_10_neg_10, texture_mouth_10_00, texture_mouth_10_10],
            [texture_mouth_03_neg_10, texture_mouth_03_00, texture_mouth_03_10],
            [texture_mouth_00_neg_10, texture_mouth_00_00, texture_mouth_00_10]
        ]
    )

    # Set Position SubData, and Draw Elements
    facemeshes = [L_pupil_mesh, L_eyelid_mesh, L_eye_mesh, R_pupil_mesh, R_eyelid_mesh, R_eye_mesh, mouth_mesh, back_hair_1_mesh, back_hair_2_mesh, front_hair_mesh, head_mesh, nose_mesh, L_ear_mesh, R_ear_mesh] # note may want to adjust draw order..
    for m in facemeshes:
        m.update_positions(positions)
        m.draw()

def close():
    #face_deform_mesh.delete()
    pass
