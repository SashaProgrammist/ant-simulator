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
    vec2 nev = vec2(cos(angel), sin(angel));
    out_direction = normalize(in_direction + nev);
}
