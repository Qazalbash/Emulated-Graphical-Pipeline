#version 300 es

precision highp float;
uniform int MAX_ITERATION;
in vec2 position;
out vec4 fragColor;

float mag(vec2 v) {
	return sqrt(v[0] * v[0] + v[1] * v[1]);
}

float mandelbrot_set(vec2 c) {
	float count = 0.0;
	float r = 0.0, t = 0.0;
	vec2 z = vec2(0.0, 0.0);
	vec2 z_ = vec2(0.0, 0.0);

	do {
		z_[0] = z[0] * z[0] - z[1] * z[1] + c[0];
		z_[1] = 2.0 * z[0] * z[1] + c[1];
		z[0] = z_[0];
		z[1] = z_[1];
		count++;
	} while(r <= 2.0 && count <= float(MAX_ITERATION));

	return count;
}

vec4 map_point_quadratic(float P, float Q, float R, vec4 A, vec4 B, vec4 C, float X) {
	float a = (X - Q) * (X - R) / (P - Q) / (P - R);
	float b = (X - P) * (X - R) / (Q - P) / (Q - R);
	float c = (X - P) * (X - Q) / (R - P) / (R - Q);
	return a * A + b * B + c * C;
}

void main() {
	vec4 red = vec4(1.0, 0.0, 0.0, 1.0);
	vec4 green = vec4(0.0, 1.0, 0.0, 1.0);
	vec4 blue = vec4(0.0, 0.0, 1.0, 1.0);

	vec2 z = vec2(position[0] * 2.0, position[1] * 2.0);

	float escape_time = mandelbrot_set(z, 2.0);

	fragColor = map_point_quadratic(1.0, float(MAX_ITERATION) / 5.0, float(MAX_ITERATION), red, green, blue, escape_time);
}