#version 330 core
layout(location = 0) in vec3 position;
//layout(location = 1) in vec2 vertex_uv;
//layout(location = 2) in vec2 aTexCoord;

//out vec2 TexCoord;

void main() {
    gl_Position = vec4(position.x, position.y, 0.0, 1.0);
    //TexCoord = aTexCoord;
}