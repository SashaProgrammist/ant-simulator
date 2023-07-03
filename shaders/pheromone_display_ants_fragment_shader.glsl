#version 400

in float v_stackingPheromoneIndex;
in vec2 v_position;
in vec2 v_direction;
uniform float pheromone;
uniform bool isPheromoneWar;
uniform vec2 resolution;
out vec4 fragColor;

void main() {
    if (isPheromoneWar) {
        vec2 correction = vec2(1, resolution.y / resolution.x);
        vec2 uv = gl_FragCoord.xy / resolution * correction;
        vec2 center = (v_position + 1) / 2 * correction;

        fragColor = vec4(vec3(1),  (0.015 - length(uv - center)) / 0.015);
    } else {
        if (v_stackingPheromoneIndex == pheromone)
            fragColor = vec4(v_direction, 0, 0.003);
    }
}
