from ctypes import byref
import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders

glfw.init()

glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, True)


gl_window = glfw.create_window(1280, 720, "Virtual Avatar Output", None, None)

if not gl_window:
    glfw.terminate()
    raise Exception("glfw window cannot be created")

glfw.set_window_pos(gl_window, 400, 200)
glfw.make_context_current(gl_window)

flags = GLint()
glGetIntegerv(GL_CONTEXT_FLAGS, byref(flags))

glClearColor(0,0.5,0.5,1)

def glDebugOutput(source, type, id, severity, length, message, userParam):
    print("msg")
    # Ignore non-significant error/warning codes
    if id == 131169 or id == 131185 or id == 131218 or id == 131204:
        return

    print("---------------")
    print("Debug message ({}): {}".format(id, message))

    if source == GL_DEBUG_SOURCE_API:
        print("Source: API")
    elif source == GL_DEBUG_SOURCE_WINDOW_SYSTEM:
        print("Source: Window System")
    elif source == GL_DEBUG_SOURCE_SHADER_COMPILER:
        print("Source: Shader Compiler")
    elif source == GL_DEBUG_SOURCE_THIRD_PARTY:
        print("Source: Third Party")
    elif source == GL_DEBUG_SOURCE_APPLICATION:
        print("Source: Application")
    elif source == GL_DEBUG_SOURCE_OTHER:
        print("Source: Other")

    print()

    if type == GL_DEBUG_TYPE_ERROR:
        print("Type: Error")
    elif type == GL_DEBUG_TYPE_DEPRECATED_BEHAVIOR:
        print("Type: Deprecated Behaviour")
    elif type == GL_DEBUG_TYPE_UNDEFINED_BEHAVIOR:
        print("Type: Undefined Behaviour")
    elif type == GL_DEBUG_TYPE_PORTABILITY:
        print("Type: Portability")
    elif type == GL_DEBUG_TYPE_PERFORMANCE:
        print("Type: Performance")
    elif type == GL_DEBUG_TYPE_MARKER:
        print("Type: Marker")
    elif type == GL_DEBUG_TYPE_PUSH_GROUP:
        print("Type: Push Group")
    elif type == GL_DEBUG_TYPE_POP_GROUP:
        print("Type: Pop Group")
    elif type == GL_DEBUG_TYPE_OTHER:
        print("Type: Other")

    print()

    if severity == GL_DEBUG_SEVERITY_HIGH:
        print("Severity: high")
    elif severity == GL_DEBUG_SEVERITY_MEDIUM:
        print("Severity: medium")
    elif severity == GL_DEBUG_SEVERITY_LOW:
        print("Severity: low")
    elif severity == GL_DEBUG_SEVERITY_NOTIFICATION:
        print("Severity: notification")

    print()

print(flags)
print(GL_CONTEXT_FLAG_DEBUG_BIT)


if flags.value & GL_CONTEXT_FLAG_DEBUG_BIT:
    print("Initialized Debug Output")
    glEnable(GL_DEBUG_OUTPUT)
    glEnable(GL_DEBUG_OUTPUT_SYNCHRONOUS)
    glDebugMessageCallback(GLDEBUGPROC(glDebugOutput), None)
    glDebugMessageControl(GL_DONT_CARE, GL_DONT_CARE, GL_DONT_CARE, 0, None, GL_TRUE)


while not glfw.window_should_close(gl_window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glUseProgram(0)
    glUniform2f(90, 1280, 720)
    glfw.swap_buffers(gl_window)
    glfw.poll_events()

glfw.terminate()