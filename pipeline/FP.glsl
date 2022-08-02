#version 300 es

precision highp float;

uniform float c_zoom;
uniform float c_x;
uniform float c_y;
uniform int nt;

in vec2 coordinate;

out vec4 fragColor;


float mag(vec2 v) {
    return sqrt(v[0] * v[0] + v[1] * v[1]);
}

float mandelbrot_set(vec2 c) {
    int count = 0;
    vec2 z = vec2(0.0, 0.0), z_ = vec2(0.0, 0.0);

    do {
        z_[0] = z[0] * z[0] - z[1] * z[1] + c[0];
        z_[1] = 2.0 * z[0] * z[1] + c[1];
        z[0] = z_[0];
        z[1] = z_[1];
        count++;
    } while(mag(z) <= 2.0 && count <= 100);

    return float(count);
}

vec4 map_point(float P, float Q, float R, vec4 A, vec4 B, vec4 C, float X) {
    float a = (X - Q) * (X - R) / ((P - Q) * (P - R));
    float b = (X - P) * (X - R) / ((Q - P) * (Q - R));
    float c = (X - P) * (X - Q) / ((R - P) * (R - Q));
    return a * A + b * B + c * C;
}

void main() {
    vec2 z = 2.0 / c_zoom * coordinate;
    z[0] = z[0] + c_x;
    z[1] = z[1] - c_y;
    float escape_time = mandelbrot_set(z);

    vec4 red = vec4(1.0, 0.0, 0.0, 1.0), green = vec4(0.0, 1.0, 0.0, 1.0), blue = vec4(0.0, 0.0, 1.0, 1.0);

    fragColor = map_point(1.0, float(nt) / 5.0, float(nt), red, green, blue, escape_time);
}