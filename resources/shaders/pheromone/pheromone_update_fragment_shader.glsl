#version 400

in vec2 v_texCoord;
uniform vec2 resolution;
uniform sampler2D mappTexture;
uniform sampler2D pheromoneTexture;
uniform float weathering;
uniform float redistribution;
uniform int redistributionRadius;
out vec4 fragColor;

void main() {
    vec3 color = vec3(0);

    if (texture(mappTexture, v_texCoord).r > 0.5) {
        for (int i = -redistributionRadius; i <= redistributionRadius; i++) {
            for (int j = -redistributionRadius; j <= redistributionRadius; j++) {
                if (i != 0 || j != 0) {
                    color += redistribution * (texture(pheromoneTexture,
                    (gl_FragCoord.xy + vec2(i, j)) / resolution).rgb - 0.5);
                } else {
                    color += weathering * (texture(pheromoneTexture, v_texCoord).rgb - 0.5);
                }
            }
        }
    }
    color += 0.5;

    fragColor = vec4(color, 1);
}
