#version 330 core
in vec2 pos;
in vec2 uv;
out vec4 fragColor;

uniform vec2 iResolution;
uniform sampler2D iChannel0;
uniform vec2 uv_start = vec2(0.0,0.0);
uniform vec2 uv_end = vec2(1.0,1.0);
float pi = 3.14159265;

void main() 
{
    //fragColor = vec4(pos.x, pos.y, 0.0, 1.0);
    //fragColor = vec4(uv.x, uv.y, 0.0, 1.0);
    //fragColor = vec4(1.0, 0.0, 0.0, 1.0);
    //fragColor = vec4(mod(uv.x, 1.0 / 8.0) ,mod(uv.y, 1.0 / 8.0), 0.0, 1.0);

    // interpolation
    uv.x = mix(uv_start.x, uv_end.x, uv.x);
    uv.y = mix(uv_start.y, uv_end.y, uv.y);
    fragColor = texture(iChannel0, uv);
    // handling transparency
    if (fragColor.a < 0.5) discard;
    /*if (fragColor == vec4(0.0,0.0,0.0,0.0)) {
        fragColor = vec4(0.0,1.0,1.0,1.0);
    }*/
}