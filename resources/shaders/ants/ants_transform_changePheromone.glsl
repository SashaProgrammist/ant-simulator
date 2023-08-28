#version 400

in float in_pheromoneControlIndex;
in vec2 in_position;
in float in_time;
uniform float foodPheromone;
uniform float homePheromone;
uniform vec2 homePosition;
uniform sampler2D mappTexture;
uniform float frame_time;
out float out_pheromoneControlIndex;
out float out_stackingPheromoneIndex;
out float out_isDirectionChanged;
out float out_time;

bool is_inHome(){
    return length(in_position - homePosition) < 0.09;
}

bool is_inFood(float food_in){
    return food_in > 0.05;
}

void main() {
    vec2 uv = (in_position + 1) / 2;
    float food_in = texture(mappTexture, uv).g;

    if (in_pheromoneControlIndex == foodPheromone) {
        if (is_inFood(food_in)) {
            out_pheromoneControlIndex = homePheromone;
            out_isDirectionChanged = 1;
            out_time = 0;
        } else {
            out_isDirectionChanged = 0;
            out_pheromoneControlIndex = foodPheromone;
            if (is_inHome()){
                out_time = 0;
            } else {
                out_time = in_time + frame_time;
            }
        }
    } else if (is_inHome()) {
        out_isDirectionChanged = 1;
        out_pheromoneControlIndex = foodPheromone;
        out_time = 0;
    } else {
        out_isDirectionChanged = 0;
        out_pheromoneControlIndex = homePheromone;
        if (is_inFood(food_in)) {
            out_time = 0;
        } else {
            out_time = in_time + frame_time;
        }
    }


    if (out_pheromoneControlIndex == foodPheromone) {
        out_stackingPheromoneIndex = homePheromone;
    } else {
        out_stackingPheromoneIndex = foodPheromone;
    }
}
