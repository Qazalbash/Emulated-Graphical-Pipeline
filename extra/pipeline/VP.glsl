#version 300 es

in vec2 vPosition;
uniform mat3 worldMatrix;
uniform mat3 viewMatrix;
uniform mat3 projectionMatrix;
out vec2 coordinate;

void main() {
    gl_Position = vec4(projectionMatrix * viewMatrix * worldMatrix * vec3(vPosition, 0.0), 1.0);
    coordinate = vPosition;
}