#version 400

in vec2 v_texCoord;
uniform sampler2D _texture;
uniform vec3 channelR;
uniform vec3 channelG;
uniform vec3 channelB;
uniform float alfa;
out vec4 fragColor;

void main() {
    vec3 color = texture(_texture, v_texCoord).rgb;
    color = color.rrr * channelR + color.ggg * channelG + color.bbb * channelB;

    fragColor = vec4(color, alfa);
}
