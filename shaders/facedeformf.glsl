#version 330 core
in vec2 pos;
in vec2 uv;
out vec4 fragColor;

uniform vec2 iResolution;
uniform sampler2D iChannel0;
float pi = 3.14159265;

void main() 
{
    //fragColor = vec4(pos.x, pos.y, 0.0, 1.0);
    //fragColor = vec4(uv.x, uv.y, 0.0, 1.0);
    //fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    //fragColor = vec4(mod(uv.x, 1.0 / 8.0) ,mod(uv.y, 1.0 / 8.0), 0.0, 1.0);
    fragColor = texture(iChannel0, uv);
}