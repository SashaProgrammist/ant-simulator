#version 400

in float in_pheromoneControlIndex;
in vec2 in_position;
uniform float foodPheromone;
uniform float homePheromone;
uniform vec2 homePosition;
uniform sampler2D mappTexture;
out float out_pheromoneControlIndex;
out float out_stackingPheromoneIndex;
out float out_isDirectionChanged;

void main() {
    if (in_pheromoneControlIndex == foodPheromone) {
        vec2 uv = (in_position + 1) / 2;
        float food_in = texture(mappTexture, uv).g;

        if (food_in > 0.05) {
            out_pheromoneControlIndex = homePheromone;
            out_isDirectionChanged = 1;
        } else {
            out_isDirectionChanged = 0;
            out_pheromoneControlIndex = foodPheromone;
        }
    } else {
        if (length(in_position - homePosition) < 0.09) {
            out_isDirectionChanged = 1;
            out_pheromoneControlIndex = foodPheromone;
        } else {
            out_isDirectionChanged = 0;
            out_pheromoneControlIndex = homePheromone;
        }
    }

    if (out_pheromoneControlIndex == foodPheromone) {
        out_stackingPheromoneIndex = homePheromone;
    } else {
        out_stackingPheromoneIndex = foodPheromone;
    }
}
