#version 400

in vec2 in_position;
in vec2 in_direction;
in float in_index;
uniform float time;
uniform float frame_time;
out vec2 out_position;

void main() {
    out_position = in_position + in_direction * frame_time;
}
