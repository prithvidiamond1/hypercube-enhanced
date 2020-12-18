# version 330

uniform mat4 projection;
uniform mat4 view;
uniform mat4 model;

uniform mat4 dbr;

in vec4 position;

out vec3 pos;

mat4 pvm = projection*view*model;
float p_factor = 2.5; // projection factor

void main() {
    vec4 trans_pos = dbr*position;
    float st_p_factor = trans_pos.w + p_factor; // stereographic projection factor
    pos = vec3(trans_pos.x, trans_pos.y, trans_pos.z)/st_p_factor;
    gl_Position = pvm*vec4(pos, 1.0);
}