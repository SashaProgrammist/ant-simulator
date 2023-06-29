#version 400

in float v_index;
in vec2 v_position;
uniform float time;
uniform float frame_time;
uniform vec2 resolution;
out vec4 fragColor;

void main() {
    fragColor = vec4(0, 0, 0, 0.5);
}
