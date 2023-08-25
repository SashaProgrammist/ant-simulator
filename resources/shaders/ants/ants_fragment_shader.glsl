#version 400

in float v_index;
in vec2 v_position;
in float v_pheromoneControlIndex;
uniform float time;
uniform float frame_time;
uniform vec2 resolution;
uniform float foodPheromone;
out vec4 fragColor;

void main() {
    if (v_pheromoneControlIndex == foodPheromone) {
        fragColor = vec4(0, 0, 0, 0.05);
    } else {
        fragColor = vec4(0.1, 0.5, 0, 0.05);
    }
}
