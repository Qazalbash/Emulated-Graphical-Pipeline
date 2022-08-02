#version 300 es

in int canvas_width;
in int canvas_height;
in float c_zoom;
in float c_x;
in float c_y;
in float c_r;

mat3 translate(float x, float y) {
    return mat3(1.0, 0.0, x, 0.0, 1.0, y, 0.0, 0.0, 1.0);
}

vec3 normalize3(vec3 v) {
    return v / length(v);
}

mat3 rotate(float angle, vec3 axis) {
    float c = cos(angle);
    float s = sin(angle);
    float t = 1.0 - c;
    vec3 v = normalize3(axis);
    float x = v.x;
    float y = v.y;
    float z = v.z;
    return mat3(t * x * x + c, t * x * y + s * z, t * x * z - s * y, t * x * y - s * z, t * y * y + c, t * y * z + s * x, t * x * z + s * y, t * y * z - s * x, t * z * z + c);
}

mat3 scale(float x, float y, float z) {
    return mat3(x, 0.0, 0.0, 0.0, y, 0.0, 0.0, 0.0, z);
}

mat3 makeCameraMatrix() {
    float zoomScale = 1 / c_zoom;
    mat3 cameraMatrix = translate(c_x, c_y);
    cameraMatrix *= rotate(c_r, vec3(0.0, 0.0, 1.0));
    cameraMatrix *= scale(zoomScale, zoomScale, 1.0);
    return cameraMatrix;
}

mat3 updateViewProjection() {
    mat3 projectionMat = mat3(1.0, 0.0, 0.0, 0.0, -1.0, 0.0, 0.0, 0.0, 1.0);
    mat3 cameraMat = makeCameraMatrix();
    mat3 viewMat = inverse(cameraMat);
    mat3 viewProjectionMat = projectionMat * viewMat;
    return viewProjectionMat;
}

void main() {

}