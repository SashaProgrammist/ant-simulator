#version 400

in vec2 in_position;
in vec2 in_direction;
in float in_index;
uniform float time;
uniform float frame_time;
out vec2 v_position;
out vec2 v_direction;
out float v_index;

void main() {
    v_position = in_position;
    v_direction = in_direction;
    v_index = in_index;
    gl_Position = vec4(v_position, 0, 1);
}
