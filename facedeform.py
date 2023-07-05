import lerp
import facedeformsurface
import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import texture

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
    global vbo, vao, ebo, textureID, shader_program
    # Import Shader
    vs_shader_src = open("shaders/facedeformv.glsl", "r").read()
    fs_shader_src = open("shaders/facedeformf.glsl", "r").read()
    shader_program = compileProgram(
        compileShader(vs_shader_src, GL_VERTEX_SHADER),
        compileShader(fs_shader_src, GL_FRAGMENT_SHADER),
        validate=False
    )
    glUseProgram(shader_program)
    # Import Texture
    textureID = texture.read_texture("skyansam.png")
    # Generate Vertexes
    positions, colors, indices = generate_points(0.0,0.0)
    # Generate Buffers
    vbo = glGenBuffers(1)
    vao = glGenVertexArrays(1)
    # Bind VAO and VBO and set vertex data
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, positions.nbytes + colors.nbytes, None, GL_DYNAMIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, positions.nbytes, positions)
    glBufferSubData(GL_ARRAY_BUFFER, positions.nbytes, colors.nbytes, colors)
    # Specify the vertex attribute pointers
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0)) # stride was 2 * 4
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(positions.nbytes))
    # Bind the index buffer
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_DYNAMIC_DRAW)
    # Unbind the VBO and VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

def update():
    global vbo, vao, ebo, shader_program, face_deform_x, face_deform_y
    # Enable Shader
    glUseProgram(shader_program)
    # Set Uniform Resolution
    iResolution_id = glGetUniformLocation(shader_program, "iResolution")
    glUniform2f(iResolution_id, 1280, 720)
    # Set Uniform Texture
    textureUniformLoc = glGetUniformLocation(shader_program, "iChannel0")
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, textureID)
    glUniform1i(textureUniformLoc, 0)
    # Generate Vertices
    positions, colors, indices = generate_points(face_deform_x,face_deform_y)
    # Bind Buffer, Set Position SubData, and Draw Elements
    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferSubData(GL_ARRAY_BUFFER, 0, positions.nbytes, positions)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    # Unbind Vertex Array and Buffer
    glBindVertexArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)

def close():
    glDeleteProgram(shader_program)
    glDeleteBuffers(1, [vbo])
    glDeleteVertexArrays(1, [vao])
