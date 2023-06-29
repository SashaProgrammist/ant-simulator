#version 400

in vec2 in_position;
in vec2 in_direction;
in float in_index;
uniform float time;
uniform float frame_time;
out vec2 out_direction;

float confusion = 0;
float random() {
    confusion += 1;
    return fract(sin(confusion * time + frame_time) * cos(in_index) * 1000);
}

void main() {
    float angel = random() * 6.28318530718;
    vec2 cos_sin = vec2(cos(angel), sin(angel));
    mat2 mat = mat2(vec2(cos_sin.x, -cos_sin.y), \
                    vec2(cos_sin.y, cos_sin.x));
    vec2 nev = mat * in_direction;
    out_direction = normalize(in_direction + nev);
}
