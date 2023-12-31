#version 400

#include shaders/ants/__pheromone_textures__.glsl

#define pi 3.14159265359
#define pi2 6.28318530718

in vec2 in_position;
in vec2 in_direction;
in float in_index;
in float in_pheromoneControlIndex;
in float in_isDirectionChanged;
uniform float time;
uniform float frame_time;
uniform sampler2D mappDirection;
uniform float sensitivityThreshold;
out vec2 out_direction;

float confusion = 0;
float random() {
    confusion += 1;
    return fract(sin(confusion * time + frame_time) * cos(in_index) * 1000);
}

void rotate(inout vec2 p, float angel) {
    vec2 cos_sin = vec2(cos(angel), sin(angel));
    mat2 mat = mat2(vec2(cos_sin.x, -cos_sin.y), \
                    vec2(cos_sin.y, cos_sin.x));
    p = mat * p;
}

void main() {
    if (in_isDirectionChanged > 0.5) {
        out_direction = -in_direction;
        return;
    }
    vec2 uv = mod((in_position + 1) / 2, 1.);
    vec2 _in_position = uv * 2 - 1;

    float angel = random() * pi2;
    vec2 randomDirection = in_direction * (1 + random()) / 2;
    rotate(randomDirection, angel);

    vec2 _mappDirection = texture(mappDirection, uv).rg;
    _mappDirection -= 0.5;
    if (length(_mappDirection) < sensitivityThreshold) {
        _mappDirection = vec2(0);
    }

    vec2 pheromoneDirection = getPheromone(in_pheromoneControlIndex, uv);
    float len = length(pheromoneDirection);
    if (len < sensitivityThreshold) {
        pheromoneDirection = vec2(0);
    }
    angel = (random() + random() - 1) * 0.9;
    rotate(pheromoneDirection, angel);

    out_direction = normalize(\
        in_direction * 1 + \
        randomDirection * 0.05 + \
        _mappDirection * 3 + \
        pheromoneDirection * 2);
}
