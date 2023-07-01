import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
import numpy as np
from scipy.interpolate import interp1d
from scipy.interpolate import CubicSpline
import texture

# CHANGE TO DYNAMIC DRAW AT SOME POINTT

is_checking_errors = True
def glCall(func, *args, **kwargs):
    function_error_checked = False
    value = None
    if is_checking_errors:
        while glGetError() != GL_NO_ERROR:
            """"""
    value = func(*args, **kwargs)
    """try:
        value = func(*args, **kwargs)
    except Exception as inst:
        print("EXCEPTION! ", inst)
        if is_checking_errors and (not function_error_checked):
            function_error_checked = True
            print("GL ERROR " + str(glGetError()))"""

    if is_checking_errors and (not function_error_checked):
        function_error_checked = True
        print("GL ERROR " + str(glGetError()))
        #opengl_error_check()
    return value


def main():
    # Initialize GLFW
    if not glfw.init():
        return

    # Create a window
    window = glfw.create_window(1280, 720, "Hello World", None, None)
    if not window:
        glfw.terminate()
        return

    # Make the window's context current
    glfw.make_context_current(window)

    # Compile shaders
    """vertex_shader = compileShader(vertex_shader_source, GL_VERTEX_SHADER)
    fragment_shader = compileShader(fragment_shader_source, GL_FRAGMENT_SHADER)

    # Create and link the shader program
    shader_program = compileProgram(vertex_shader, fragment_shader)"""

    vs_shader_src = open("shaders/facedeformv.glsl", "r").read()
    fs_shader_src = open("shaders/facedeformf.glsl", "r").read()
    shader_program = compileProgram(
        compileShader(vs_shader_src, GL_VERTEX_SHADER),
        compileShader(fs_shader_src, GL_FRAGMENT_SHADER),
        validate=False
    )
    glCall(glUseProgram,shader_program)
    

    textureID = texture.read_texture("skyansam.png")
    # Define the vertices of the triangle
    

    positions = np.array([
        -1.0, -1.0, # Bottom left
        1.0, 1.0,  # Bottom right
        -1.0, 1.0, # Top center
    ], dtype=np.float32)

    colors = np.array([
        0.0, 1.0,
        1.0, 0.0,
        1.0, 1.0
    ], dtype=np.float32)

    # Define the indices of the triangle
    indices = np.array([
        0, 1, 2  # Triangle indices
    ], dtype=np.uint32)

    """
    ## BEGIN FACE

    p2scale = [0, 1.0]
    p4scale = [0, 0.33, 0.66, 1.0]
    topLineLerpX = CubicSpline(p4scale, [72.0 / 400.0, 160.0 / 400.0, 245.0 / 400.0, 330.0 / 400.0])
    topLineLerpY = CubicSpline(p4scale, [14.0 / 400.0, 14.0 / 400.0, 14.0 / 400.0, 14.0 / 400.0])
    bottomLineLerpX = CubicSpline(p4scale, [53.0 / 400.0, 151.0 / 400.0, 251.0 / 400.0, 352.0 / 400.0])
    bottomLineLerpY = CubicSpline(p4scale, [370.0 / 400.0, 332.0 / 400.0, 332.0 / 400.0, 370.0 / 400.0])

    print(72.0/400.0)
    print(160.0/400.0)
    print(245.0/400.0)


    
    positions = []
    colors = []

    for y in range(9):
        for x in range(9):
            tX = float(x) / 8.0
            tY = float(y) / 8.0
            topLineX = topLineLerpX(tX)
            topLineY = topLineLerpY(tX)
            bottomLineX = bottomLineLerpX(tX)
            bottomLineY = bottomLineLerpY(tX)
            ptX = interp1d(p2scale, [bottomLineX, topLineX], kind="linear")(tY)
            ptY = interp1d(p2scale, [bottomLineY, topLineY], kind="linear")(tY)
            positions.append(float(ptX))
            positions.append(float(ptY))
            colors.append(tX)
            colors.append(tY)

    def get_index(x, y):
        return (y * 8) + x

    indices = []

    # Y = 0, X = 0 - 3 will display, no other triangles display.. Likely something with vertices or index values..
    # check vertices to see if valid, check indices to see if makes sense, check get indices function.. culling should be disabled for now..
    for y in range(0, 8):
        for x in range(0, 8):
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


    ## END FACE
    """

    # Create vertex buffer object (VBO) and vertex array object (VAO)
    vbo = glGenBuffers(1)
    vao = glGenVertexArrays(1)

    # Bind the VAO
    glBindVertexArray(vao)

    # Bind the VBO and set the vertex data
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    #glBufferData(GL_ARRAY_BUFFER, positions.nbytes, positions, GL_STATIC_DRAW)

    
    #glBufferData(GL_ARRAY_BUFFER, positions.nbytes + colors.nbytes, np.empty(positions.size + colors.size, dtype=np.float32), GL_STATIC_DRAW)
    #print("BUF SIZE : ", glGetBufferParameteriv(GL_ARRAY_BUFFER, GL_BUFFER_SIZE))
    glBufferData(GL_ARRAY_BUFFER, positions.nbytes + colors.nbytes, None, GL_STATIC_DRAW)
    glBufferSubData(GL_ARRAY_BUFFER, 0, positions.nbytes, positions)
    glBufferSubData(GL_ARRAY_BUFFER, positions.nbytes, colors.nbytes, colors)
    

    # Specify the vertex attribute pointers
    glEnableVertexAttribArray(0)
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0)) # stride was 2 * 4
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(positions.nbytes)) #

    

    # Bind the index buffer
    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

    # Unbind the VBO and VAO
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Set the clear color
    glClearColor(0.2, 0.3, 0.3, 1.0)

    # Enable depth testing
    #glEnable(GL_DEPTH_TEST)

    print(positions)
    print(colors)
    print(indices)

    # Render loop
    while not glfw.window_should_close(window):
        # Clear the color and depth buffers
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glDisable(GL_CULL_FACE)

        # Use the shader program
        glUseProgram(shader_program)


        iResolution_id = glGetUniformLocation(shader_program, "iResolution")
        glUniform2f(iResolution_id, 1280, 720)

        textureUniformLoc = glGetUniformLocation(shader_program, "iChannel0")
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, textureID)
        glUniform1i(textureUniformLoc, 0)

        # Bind the VAO
        glBindVertexArray(vao)

        # Draw the triangle
        glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)

        # Unbind the VAO
        glBindVertexArray(0)

        # Swap the front and back buffers
        glfw.swap_buffers(window)

        # Poll for and process events
        glfw.poll_events()
        

    # Clean up
    glDeleteProgram(shader_program)
    glDeleteBuffers(1, [vbo])
    glDeleteVertexArrays(1, [vao])
    glfw.terminate()


if __name__ == "__main__":
    main()