#version 300 es

in vec2 vPosition;
out vec2 position;

void main() {
	gl_Position = vec4(vPosition, 0.0, 1.0);
	gl_PointSize = 1.0;
	position = vPosition;
}