#version 400

in vec2 v_texCoord;
out vec4 fragColor;

void main() {
    vec4 color = vec4(150./255, 75./255, 0, (0.9 - length(v_texCoord)) * 10);

    fragColor = color;
}
