#version 300 es

in vec2 vPosition;
in vec4 vColor;
out vec4 colors;

void main() {
	gl_Position = vec4(vPosition, 0.0, 1.0);
	colors = vColor;
	gl_PointSize = 1.0;
}