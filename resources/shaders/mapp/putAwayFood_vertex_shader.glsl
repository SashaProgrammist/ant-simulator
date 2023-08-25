#version 400

in float in_isDirectionChanged;
in vec2 in_position;
uniform sampler2D mappTexture;
out vec4 color;

void main() {
    if (in_isDirectionChanged > 0.5) {
        gl_Position = vec4(in_position, 0, 1);

        vec2 uv = (in_position + 1) / 2;
        vec3 colorMapp = texture(mappTexture, uv).rgb;
        color = vec4(colorMapp.r, colorMapp.g * 0.9, colorMapp.b, 1 - colorMapp.g * 0.99);
    } else {
        gl_Position = vec4(2);
    }
}
