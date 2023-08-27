#version 400

#define pi 3.14159265359
#define pi2 6.28318530718

in float in_isDirectionChanged;
in vec2 in_position;
in float in_index;
uniform sampler2D mappTexture;
uniform float time;
uniform float frame_time;
out vec4 color;

float confusion = 0;
float random() {
    confusion += 1;
    return fract(sin(confusion * time + in_index) * cos(frame_time * 1000) * 789);
}

void rotate(inout vec2 p, float angel) {
    vec2 cos_sin = vec2(cos(angel), sin(angel));
    mat2 mat = mat2(vec2(cos_sin.x, -cos_sin.y), \
                    vec2(cos_sin.y, cos_sin.x));
    p = mat * p;
}

void main() {
    if (in_isDirectionChanged > 0.5) {
        float angel = random() * pi2;
        vec2 randomDirection = vec2((1 + random()) / 2, 0);
        rotate(randomDirection, angel);

        gl_Position = vec4(in_position + randomDirection / 200, 0, 1);

        vec2 uv = (in_position + 1) / 2;


        vec3 colorMapp = texture(mappTexture, uv).rgb;
        color = vec4(colorMapp.r, colorMapp.g * 0.9, colorMapp.b, 1 - colorMapp.g * 0.9);
    } else {
        gl_Position = vec4(2);
    }
}
