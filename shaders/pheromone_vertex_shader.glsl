#version 400

in vec2 in_position;
in float in_pheromone;
out float v_pheromone;

void main() {
    gl_Position = vec4(mod((in_position + 1) / 2, 1.) * 2 - 1, 0, 1);
    v_pheromone = in_pheromone;
}
