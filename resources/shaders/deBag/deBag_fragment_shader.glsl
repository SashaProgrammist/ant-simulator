#version 400

in vec2 v_texCoord;
in vec2 v_position;
uniform sampler2D _texture;
out vec4 fragColor;

void main() {
    vec4 color = vec4(texture(_texture, v_texCoord).rrr, 0);

    fragColor = color;
}