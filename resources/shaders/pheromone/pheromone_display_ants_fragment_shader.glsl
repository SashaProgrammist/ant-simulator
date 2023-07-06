#version 400

in vec4 collor;
in vec2 v_position;
uniform float pheromone;
uniform bool isPheromoneWar;
uniform vec2 resolution;
uniform float time;
uniform float frame_time;
out vec4 fragColor;

void main() {
    if (isPheromoneWar) {
        vec2 correction = vec2(1, resolution.y / resolution.x);
        vec2 uv = gl_FragCoord.xy / resolution * correction;
        vec2 center = (v_position + 1) / 2 * correction;

        fragColor = vec4(vec3(1), (0.015 - length(uv - center)) / 0.015);
    } else {
        fragColor = collor;
    }
}
