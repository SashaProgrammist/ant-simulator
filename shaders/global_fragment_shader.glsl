#version 400

#define pi 3.14159265359
#define pi2 6.28318530718

in vec2 v_texCoord;
in vec2 v_position;
uniform sampler2D pheromone;
uniform vec2 resolution;
out vec4 fragColor;

void main() {
//    vec2 mappDirection = vec2(0);
//    float radius = 0.03;
//    float density = 0.001;
//    float levels = 3.;
//    for (int i = 1; i <= levels; i++) {
//        float currentRadius = (i / levels) * radius;
//        float lengthCircle = currentRadius * pi2;
//        float countPoint = ceil(lengthCircle / density) - 1.;
//        for (int j = 0; j < countPoint; j++) {
//            float radian = j * pi2 / countPoint;
//            vec2 ovset = vec2(cos(radian), sin(radian));
//            vec2 point = ovset * currentRadius + v_position;
//
//            float mapp = 1 - texture(mappTexture, (point + 1) / 2).r;
//
//            mappDirection += -ovset * mapp / currentRadius;
//        }
//    }
//    vec4 color = vec4(mappDirection / 10000 + 0.5, 0, 1);
    vec4 color = vec4(texture(pheromone, v_texCoord).rgb, 0);

    fragColor = color;
}
