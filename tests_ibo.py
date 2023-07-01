import numpy as np
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram

# Vertex shader source code
vertex_shader_source = """
#version 330 core

layout (location = 0) in vec2 position;
layout (location = 1) in vec2 color;

out vec2 frag_color;

void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
    frag_color = color;
}
"""

# Fragment shader source code
fragment_shader_source = """
#version 330 core

in vec2 frag_color;
out vec4 out_color;

void main()
{
    out_color = vec4(frag_color, 1.0, 1.0);
}
"""

glfw.init()

# Configure GLFW
glfw.window_hint(glfw.VISIBLE, False)
glfw.window_hint(glfw.RESIZABLE, False)

# Create a window
window = glfw.create_window(800, 600, "PyOpenGL IBO Example", None, None)

# Make the OpenGL context current
glfw.make_context_current(window)

# Compile and link the shaders
vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)
shader_program = compileProgram(vertex_shader, fragment_shader)

# Vertex data
vertices = np.array([
    # Position     Color
    -0.5, -0.5,     1.0, 0.0,   # Vertex 1
    0.5, -0.5,      0.0, 1.0,   # Vertex 2
    0.5, 0.5,       0.0, 0.0,   # Vertex 3
    -0.5, 0.5,      1.0, 1.0    # Vertex 4
], dtype=np.float32)

# Index data
indices = np.array([
    0, 1, 2,    # Triangle 1
    2, 3, 0     # Triangle 2
], dtype=np.uint32)

# Create the Vertex Array Object (VAO) and bind it
vao = glGenVertexArrays(1)
glBindVertexArray(vao)

# Create the Vertex Buffer Object (VBO) and bind it
vbo = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

# Enable the vertex attribute arrays
glEnableVertexAttribArray(0)
glEnableVertexAttribArray(1)

# Set the attribute pointers for position and color
glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(0))
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 16, ctypes.c_void_p(8))

# Create the Index Buffer Object (IBO) and bind it
ibo = glGenBuffers(1)
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ibo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

# Unbind the VAO
glBindVertexArray(0)

# Set the clear color
glClearColor(0.0, 0.0, 0.0, 1.0)

while not glfw.window_should_close(window):
    print("we")

    # Clear the buffer
    glClear(GL_COLOR_BUFFER_BIT)

    # Bind the shader program and VAO
    glUseProgram(shader_program)
    glBindVertexArray(vao)

    # Draw the triangles using the IBO
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

    # Unbind the shader program and VAO
    glBindVertexArray(0)
    glUseProgram(0)

    # Swap buffers
    # Swap the front and back buffers
    glfw.swap_buffers(window)

    # Poll for and process events
    glfw.poll_events()

# Terminate GLFW
glfw.terminate()

#if __name__ == '__main__':
    #main()