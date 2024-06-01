import texture
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileShader, compileProgram
class Mesh:
    def __init__(self, positions, colors, indices, texture_id, start_uv, end_uv, shader_vs_filename, shader_fs_filename):
        self.positions = positions
        self.colors = colors
        self.indices = indices
        self.textureID = texture_id
        self.uv_start = start_uv
        self.uv_end = end_uv
        self.shader_program = compileProgram(
            compileShader(open(shader_vs_filename, "r").read(), GL_VERTEX_SHADER),
            compileShader(open(shader_fs_filename, "r").read(), GL_FRAGMENT_SHADER),
            validate=False
        )
        self.vbo = glGenBuffers(1)
        self.vao = glGenVertexArrays(1)
        # Bind VAO and VBO and set vertex data
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, positions.nbytes + colors.nbytes, None, GL_DYNAMIC_DRAW)
        glBufferSubData(GL_ARRAY_BUFFER, 0, positions.nbytes, positions)
        glBufferSubData(GL_ARRAY_BUFFER, positions.nbytes, colors.nbytes, colors)
        # Specify the vertex attribute pointers
        glEnableVertexAttribArray(0)
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0)) # stride was 2 * 4
        glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(positions.nbytes))
        # Bind the index buffer
        self.ebo = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_DYNAMIC_DRAW)
        # Unbind the VBO and VAO
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

    def update_positions(self, positions):
        if (self.positions.nbytes == positions.nbytes):
            self.positions = positions
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferSubData(GL_ARRAY_BUFFER, 0, positions.nbytes, positions)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
        else:
            print("Number of bytes of positions is incorrect")
        
    def update_colors(self, colors):
        if (self.colors.nbytes == colors.nbytes):
            self.colors = colors
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
            glBufferSubData(GL_ARRAY_BUFFER, self.positions.nbytes, colors.nbytes, colors)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
        else:
            print("Number of bytes of colors is incorrect")
    
    def update_indices(self, indices):
        if (self.indices.nbytes == indices.nbytes):
            self.indices = indices
            glBindVertexArray(self.vao)
            glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
            glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_DYNAMIC_DRAW)
            glBindBuffer(GL_ARRAY_BUFFER, 0)
            glBindVertexArray(0)
        else:
            print("Number of bytes of indices is incorrect")
    
    def draw(self):
        # Enable Shader
        glUseProgram(self.shader_program)
        # Set Uniform Texture
        textureUniformLoc = glGetUniformLocation(self.shader_program, "iChannel0")
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_2D, self.textureID)
        glUniform1i(textureUniformLoc, 0)
        # Set Min/Max UV Coordinates
        uvMinLoc = glGetUniformLocation(self.shader_program, "uv_start")
        uvMaxLoc = glGetUniformLocation(self.shader_program, "uv_end")
        glUniform2f(uvMinLoc, self.uv_start[0], self.uv_start[1])
        glUniform2f(uvMaxLoc, self.uv_end[0], self.uv_end[1])
        # Draw Mesh
        glBindVertexArray(self.vao)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glDrawElements(GL_TRIANGLES, len(self.indices), GL_UNSIGNED_INT, None)
        glBindVertexArray(0)
        glBindBuffer(GL_ARRAY_BUFFER, 0)
    
    def delete(self):
        glDeleteProgram(self.shader_program)
        glDeleteBuffers(1, [self.vbo])
        glDeleteVertexArrays(1, [self.vao])
        

