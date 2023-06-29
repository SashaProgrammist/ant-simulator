#version 400

in vec2 in_position;
in vec2 in_direction;
in float in_index;
uniform float time;
uniform float frame_time;

void main() {
    gl_Position = vec4(in_position, 0, 1);
}
