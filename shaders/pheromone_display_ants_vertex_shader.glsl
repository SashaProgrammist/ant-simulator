#version 400

in vec2 in_position;
in float in_stackingPheromoneIndex;
out float v_stackingPheromoneIndex;
out vec2 v_position;

void main() {
    v_position = mod((in_position + 1) / 2, 1.) * 2 - 1;
    gl_Position = vec4(v_position, 0, 1);
    v_stackingPheromoneIndex = in_stackingPheromoneIndex;
}
