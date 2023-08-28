#version 400

in vec2 in_position;
in float in_stackingPheromoneIndex;
in vec2 in_direction;
in float in_index;
in float in_time;
uniform float pheromone;
uniform sampler2D pheromoneSampler;
uniform bool isPheromoneWar;
uniform float time;
uniform float frame_time;
out vec4 collor;
out vec2 v_position;

float countFusion = 0;
float random() {
    countFusion += 1;
    return fract(sin(countFusion * frame_time + time * cos(in_index)) *
    sin(in_index + 0.58) * 957);
}

void main() {
    v_position = in_position;
    gl_Position = vec4(v_position, 0, 1);
    collor = vec4(-in_direction / 2 + 0.5, 0, frame_time);

    vec3 collorIn = texture(pheromoneSampler, (v_position + 1) / 2).rgb;
    float factor = collorIn.b * collorIn.b;

    collor.rg = collor.rg * (1 - factor) + collorIn.rg * factor * 0.95;

    if (random() - 0.5 > (2 - 2 / (1 + exp(-in_time / 10)))) {
        collor.a = 0;
    }

    if (isPheromoneWar) {
        if (collorIn.r > 0.99) {
            gl_Position = vec4(2);
        }
    } else if (in_stackingPheromoneIndex != pheromone) {
        gl_Position = vec4(2);
    } else if (random() > 0.8) {
        collor.b = 1;
    } else {
        collor.b = collorIn.b;
    }


}
