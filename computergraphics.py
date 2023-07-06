import math
import glfw
from OpenGL.GL import *
from OpenGL.GL import shaders
import facedeform
import time
import lerp
global gl_window 
gl_window = None

face_deform_x = 0.0
face_deform_y = 0.0

def start():
    global gl_window
    glfw.init()
    gl_window = glfw.create_window(720, 720, "Virtual Avatar Output", None, None)

    if not gl_window:
        glfw.terminate()
        raise Exception("glfw window cannot be created")

    glfw.set_window_pos(gl_window, 400, 200)
    glfw.make_context_current(gl_window)

    glClearColor(0,0.5,0.5,1)

    facedeform.start()

def is_window_open():
    return not glfw.window_should_close(gl_window)

def update():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDisable(GL_CULL_FACE)
    #glAlphaFunc()

    facedeform.face_deform_x = lerp.lerp2_1d(facedeform.face_deform_x,face_deform_x,0.5)
    facedeform.face_deform_y = lerp.lerp2_1d(facedeform.face_deform_y,face_deform_y,0.5)

    #facedeform.face_deform_x = math.sin(time.time())
    #facedeform.face_deform_y = math.cos(time.time())
    facedeform.update()

    glfw.swap_buffers(gl_window)
    glfw.poll_events()

def end():
    facedeform.close()
    glfw.terminate()