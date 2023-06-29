#version 400

uniform sampler2D mappTexture;
uniform vec2 resolution;
out vec4 fragColor;

void main() {
    fragColor =
    vec4(texture(mappTexture, gl_FragCoord.xy / resolution).rgb, 1);
}
