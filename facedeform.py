from scipy.interpolate import interp1d
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import texture

vbo = 0
ibo = 0
program_id = None
sizeoffloat = 4
sizeofint = 4

def start():
    global vbo
    global ibo
    global program_id

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    pos_attr = 0
    glEnableVertexAttribArray(pos_attr)
    glVertexAttribPointer(pos_attr, 2, GL_FLOAT, GL_FALSE, 0, 0) # revise?
    
    
    uv_attr = 1
    glEnableVertexAttribArray(uv_attr)
    glVertexAttribPointer(uv_attr, 2, GL_FLOAT, GL_FALSE, 0, 8) # revise?
    
    
    ibo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)

    vs_shader_src = open("shaders/facedeformv.glsl", "r").read()
    fs_shader_src = open("shaders/facedeformf.glsl", "r").read()
    program_id = shaders.compileProgram(
        shaders.compileShader(vs_shader_src, GL_VERTEX_SHADER),
        shaders.compileShader(fs_shader_src, GL_FRAGMENT_SHADER),
        validate=False
    )
    
    texture.read_texture("skyansam.png") #Handles gl stuff (unsure if i need uniform1i?)

def update():
    global vbo
    global ibo
    global program_id

    p2scale = np.array([0, 1.0])
    p4scale = np.array([0, 0.33, 0.66, 1.0])
    topLineLerpX = interp1d(p4scale, [72.0 / 400.0, 160.0 / 400.0, 245.0 / 400.0, 330.0 / 400.0], kind='linear')
    topLineLerpY = interp1d(p4scale, [14.0 / 400.0, 14.0 / 400.0, 14.0 / 400.0, 14.0 / 400.0], kind='linear')
    bottomLineLerpX = interp1d(p4scale, [53.0 / 400.0, 151.0 / 400.0, 251.0 / 400.0, 352.0 / 400.0], kind='linear')
    bottomLineLerpY = interp1d(p4scale, [370.0 / 400.0, 332.0 / 400.0, 332.0 / 400.0, 370.0 / 400.0], kind='linear')

    vertices = []

    for y in range(0, 9):
        for x in range(0, 9):
            tX = float(x) / 8.0
            tY = float(y) / 8.0
            topLineX = topLineLerpX(tX)
            topLineY = topLineLerpY(tX)
            bottomLineX = bottomLineLerpX(tX)
            bottomLineY = bottomLineLerpY(tX)
            ptX = interp1d(p2scale, [bottomLineX, topLineX], kind='linear')(tY)
            ptY = interp1d(p2scale, [bottomLineY, topLineY], kind='linear')(tY)
            vertices.append(float(ptX))
            vertices.append(float(ptY))
            vertices.append(tX)
            vertices.append(tY)

    def get_index(x, y):
        return (y * 8) + x

    indices = []

    for x in range(0, 8):
        for y in range(0, 8):
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

    vertices = np.array(vertices, dtype=np.float32)
    indices = np.array(indices, dtype=np.uint32)

    glUseProgram(program_id)
    glDisable(GL_CULL_FACE)
    iResolution_id = glGetUniformLocation(program_id, "iResolution")
    glUniform2f(iResolution_id, 1280, 720)

    
    #glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
    #glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    glDrawElements(GL_TRIANGLES, indices.size, GL_UNSIGNED_INT, None)
    
    #glfw.swapBuffers(window)
    #glfw.pollEvents()


