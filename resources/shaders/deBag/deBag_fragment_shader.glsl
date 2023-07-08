#version 400

in vec2 v_texCoord;
uniform sampler2D _texture;
uniform vec3 chanelR;
uniform vec3 chanelG;
uniform vec3 chanelB;
out vec4 fragColor;

void main() {
    vec3 color = texture(_texture, v_texCoord).rgb;
    color = color.rrr * chanelR + color.ggg * chanelG + color.bbb * chanelB;

    fragColor = vec4(color, 1);
}
