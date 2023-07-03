#version 400

in vec2 in_position;
in float in_pheromone;
out float v_pheromone;
out vec2 v_position;

void main() {
    v_position = mod((in_position + 1) / 2, 1.) * 2 - 1;
    gl_Position = vec4(v_position, 0, 1);
    v_pheromone = in_pheromone;
}
