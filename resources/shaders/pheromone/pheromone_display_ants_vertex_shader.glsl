#version 400

in vec2 in_position;
in float in_stackingPheromoneIndex;
in vec2 in_direction;
uniform sampler2D pheromoneSampler;
uniform bool isPheromoneWar;
out vec2 v_direction;
out float v_stackingPheromoneIndex;
out vec2 v_position;

void main() {
    v_position = in_position;
    gl_Position = vec4(v_position, 0, 1);
    v_stackingPheromoneIndex = in_stackingPheromoneIndex;
    v_direction = -in_direction / 2 + 0.5;

    if (isPheromoneWar) {
        if (texture(pheromoneSampler, (v_position + 1) / 2).r > 0.99) {
            gl_Position = vec4(2);
        }
    }
}
