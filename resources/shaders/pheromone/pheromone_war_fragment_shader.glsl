#version 400

in vec2 v_texCoord;
in vec2 v_position;
uniform sampler2D pheromone;
out vec4 fragColor;

void main() {
    vec4 color = vec4(vec3(0), 1 - texture(pheromone, v_texCoord).r);

    fragColor = color;
}
