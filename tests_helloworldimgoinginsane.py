import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(800, 600, "Hello World Triangle", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Compile shaders
    """
    vertex_shader = """
    #version 330
    #layout(location = 0) in vec3 position;
    #void main()
    #{
    #    gl_Position = vec4(position, 1.0);
    #}
    """

    fragment_shader = """
    #version 330
    #out vec4 fragColor;
    #void main()
    #{
    #    fragColor = vec4(1.0, 0.5, 0.2, 1.0);
    #}
    """

    shader_program = compileProgram(
        compileShader(vertex_shader, GL_VERTEX_SHADER),
        compileShader(fragment_shader, GL_FRAGMENT_SHADER)
    )
    """

    vs_shader_src = open("shaders/facedeformv.glsl", "r").read()
    fs_shader_src = open("shaders/facedeformf.glsl", "r").read()
    shader_program = shaders.compileProgram(
        shaders.compileShader(vs_shader_src, GL_VERTEX_SHADER),
        shaders.compileShader(fs_shader_src, GL_FRAGMENT_SHADER),
        validate=False
    )
    glCall(glUseProgram,shader_program)
    # Define the vertices of the triangle
    vertices = [
        -0.5, -0.5, 0.0,  # bottom left
        0.5, -0.5, 0.0,   # bottom right
        0.0, 0.5, 0.0     # top center
    ]

    # Convert the vertices to a NumPy array
    vertices = np.array(vertices, dtype=np.float32)

    # Create a vertex buffer object (VBO) and bind it
    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)

    # Upload the vertex data to the VBO
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    # Create a vertex array object (VAO) and bind it
    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    # Enable the vertex attribute array at location 0
    glEnableVertexAttribArray(0)

    # Specify the layout of the vertex data
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

    # Set the clear color
    glClearColor(0.2, 0.3, 0.3, 1.0)

    # Enable depth testing
    glEnable(GL_DEPTH_TEST)

    # Main loop
    while not glfw.window_should_close(window):
        # Clear the color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Use the shader program
        glUseProgram(shader_program)

        # Bind the vertex array object
        glBindVertexArray(vao)

        # Draw the triangle
        glDrawArrays(GL_TRIANGLES, 0, 3)

        # Swap the front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()

    # Cleanup
    glDeleteVertexArrays(1, [vao])
    glDeleteBuffers(1, [vbo])
    glDeleteProgram(shader_program)

    # Terminate GLFW
    glfw.terminate()


if __name__ == '__main__':
    main()