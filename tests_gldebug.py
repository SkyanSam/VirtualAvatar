from OpenGL import GL as gl
import glfw

def cb_dbg_msg(source, msg_type, msg_id, severity, length, raw, user):
    msg = raw[0:length]
    print("debug", source, msg_type, msg_id, severity, msg)

def main():
    glfw.init()
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 2)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
    glfw.window_hint(glfw.OPENGL_DEBUG_CONTEXT, True)

    window = glfw.create_window(640, 480, "test", None, None)
    glfw.make_context_current(window)

    # Install our debug message callback
    gl.glDebugMessageCallback(gl.GLDEBUGPROC(cb_dbg_msg), None)

    # This shader program doesn't exist, so you can expect the debug
    # message callback to receive an error message
    gl.glUseProgram(1234)

    while not glfw.window_should_close(window):
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
