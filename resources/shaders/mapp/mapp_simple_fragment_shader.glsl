#version 400

in vec2 v_texCoord;
uniform sampler2D mappTexture;
uniform vec2 resolution;
out vec4 fragColor;

void main() {
    vec4 color = texture(mappTexture, v_texCoord);
    
//    temp
    fragColor = vec4(color.rrr, 1);
    if (color.g > 0.5)
        fragColor = vec4(0, 1, 0, 1);
}
