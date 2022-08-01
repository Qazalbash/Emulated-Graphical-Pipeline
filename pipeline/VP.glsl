#version 300 es

in vec2 vPosition;
uniform mat3 matrix;
out vec2 coordinate;

void main() {
    gl_Position = vec4(matrix * vec3(vPosition, 0.0), 1.0);
    gl_PointSize = 1.0;
    coordinate = vPosition;
}