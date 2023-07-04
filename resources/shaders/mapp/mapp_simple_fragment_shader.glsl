#version 400

in vec2 v_texCoord;
uniform sampler2D mappTexture;
uniform vec2 resolution;
out vec4 fragColor;

void main() {
    fragColor = vec4(texture(mappTexture, v_texCoord).rgb, 1);
}
