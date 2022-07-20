

#version 300 es

precision highp float;
in vec4 colors;

void main() {
	gl_FragColor = colors;
}
