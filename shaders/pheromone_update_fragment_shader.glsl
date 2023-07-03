#version 400

in vec2 v_texCoord;
uniform vec2 resolution;
uniform sampler2D mappTexture;
uniform sampler2D pheromoneTexture;
uniform float weathering;
uniform float redistribution;
out vec4 fragColor;

void main() {
    vec3 color = vec3(0);

    if (texture(mappTexture, v_texCoord).r > 0.5) {
        for (int i = -1; i < 2; i++) {
            for (int j = -1; j < 2; j++) {
                if (i != 0 || j != 0) {
                    color += redistribution * (texture(pheromoneTexture,
                    (gl_FragCoord.xy + vec2(i, j)) / resolution).rgb - 0.5);
                } else {
                    color += (texture(pheromoneTexture, v_texCoord).rgb - 0.5);
                }
            }
        }
    }
    color *= weathering;
    color += 0.5;

    fragColor = vec4(color, 1);
}
