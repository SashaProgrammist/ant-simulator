#version 400

in float in_index;
uniform float time;
uniform float frame_time;
out vec4 fragColor;

void main() {
    fragColor = vec4(0, 0, 0, 0.5);
}
