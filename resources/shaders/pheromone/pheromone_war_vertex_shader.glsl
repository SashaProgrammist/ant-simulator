#version 400

in vec3 in_position;
in vec2 in_texCoord;
out vec2 v_texCoord;

void main() {
    gl_Position = vec4(in_position, 1);
    v_texCoord = in_texCoord;
}
