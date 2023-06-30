import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders

global gl_window 
gl_window = None

def start():
    global gl_window
    glfw.init()
    gl_window = glfw.create_window(1280, 720, "Virtual Avatar Output", None, None)

    if not gl_window:
        glfw.terminate()
        raise Exception("glfw window cannot be created")

    glfw.set_window_pos(gl_window, 400, 200)
    glfw.make_context_current(gl_window)

    glClearColor(0,0.5,0.5,1)

def is_window_open():
    return not glfw.window_should_close(gl_window)

def update():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glfw.swap_buffers(gl_window)
    glfw.poll_events()

def close():
    glfw.terminate()