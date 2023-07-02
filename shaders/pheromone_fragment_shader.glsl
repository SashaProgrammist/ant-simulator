#version 400

in float v_pheromone;
uniform float pheromone;
uniform bool isPheromoneWar;
out vec4 fragColor;

void main() {
    if (isPheromoneWar) {
        fragColor = vec4(1, 1, 1, 0.01);
    } else {
        if (v_pheromone == pheromone)
            fragColor = vec4(1, 1, 1, 0.01);
    }
}
