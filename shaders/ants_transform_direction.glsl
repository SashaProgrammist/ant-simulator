#version 400

#define pi 3.14159265359
#define pi2 6.28318530718

in vec2 in_position;
in vec2 in_direction;
in float in_index;
uniform float time;
uniform float frame_time;
uniform sampler2D mappTexture;
out vec2 out_direction;

float confusion = 0;
float random() {
    confusion += 1;
    return fract(sin(confusion * time + frame_time) * cos(in_index) * 1000);
}

void main() {
    vec2 _in_position = mod((in_position + 1) / 2, 1.) * 2 - 1;

    float angel = random() * pi2;
    vec2 cos_sin = vec2(cos(angel), sin(angel));
    mat2 mat = mat2(vec2(cos_sin.x, -cos_sin.y), \
                    vec2(cos_sin.y, cos_sin.x));
    vec2 randomDirection = mat * in_direction;

    vec2 mappDirection = vec2(0);
    float radius = 0.03;
    float density = 0.002;
    float levels = 4.;
    for (int i = 1; i <= levels; i++) {
        float currentRadius = (i / levels) * radius;
        float lengthCircle = currentRadius * pi2;
        float countPoint = ceil(lengthCircle / density) - 1.;
        for (int j = 0; j < countPoint; j++) {
            float radian = j * pi2 / countPoint;
            vec2 ovset = vec2(cos(radian), sin(radian));
            vec2 point = ovset * currentRadius + _in_position;

            float mapp = 1 - texture(mappTexture, (point + 1) / 2).r;

            mappDirection += -ovset * mapp / currentRadius * radius * 0.025;
        }
    }

    out_direction = normalize(in_direction + randomDirection * 0.1 + mappDirection);
}
