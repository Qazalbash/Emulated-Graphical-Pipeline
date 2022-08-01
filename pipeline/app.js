"use strict";

let gl, vertices;
let nt = 100;
var program;

const camera = {
    x: 0.0,
    y: 0.0,
    rotation: 0.0,
    zoom: 1.0,
};

window.onload = function init() {
    var canvas = document.getElementById("set");
    gl = canvas.getContext("webgl2");

    if (!gl) {
        alert("WebGL 2.0 is not available");
    }

    vertices = [
        vec2(-1.0, 1.0),
        vec2(1.0, 1.0),
        vec2(1.0, -1.0),
        vec2(-1.0, -1.0),
    ];

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    program = initShaders(gl, "vShader", "fShader");
    gl.useProgram(program);

    render();
};

function projection() {
    // Note: This matrix flips the Y axis so 0 is at the top.
    return [1, 0, 0, 0, -1, 0, 0, 0, 1];
}

function transformPoint(m, v) {
    var v0 = v[0];
    var v1 = v[1];
    // var d = v0 * m[0 * 3 + 2] + v1 * m[1 * 3 + 2] + m[2 * 3 + 2];
    var d = v0 * m[2] + v1 * m[5] + m[8];

    // return [
    // 	(v0 * m[0 * 3 + 0] + v1 * m[1 * 3 + 0] + m[2 * 3 + 0]) / d,
    // 	(v0 * m[0 * 3 + 1] + v1 * m[1 * 3 + 1] + m[2 * 3 + 1]) / d,
    // ];
    return [
        (v0 * m[0] + v1 * m[3] + m[6]) / d,
        (v0 * m[1] + v1 * m[4] + m[7]) / d,
    ];
}

function makeCameraMatrix() {
    const zoomScale = 1 / camera.zoom;
    let cameraMat = mat3(1, 0, 0, 0, 1, 0, 0, 0, 1);
    cameraMat = mult(cameraMat, translate(camera.x, camera.y));
    cameraMat = mult(cameraMat, rotate(camera.rotation, vec3(0, 0, 1), 3));
    cameraMat = mult(cameraMat, scale(zoomScale, zoomScale));
    return cameraMat;
}

function updateViewProjection() {
    // same as ortho(0, width, height, 0, -1, 1)
    const projectionMat = mat3(projection());
    const cameraMat = makeCameraMatrix();
    let viewMat = inverse3(cameraMat);
    viewProjectionMat = mult(projectionMat, viewMat);
}

canvas.addEventListener("wheel", (e) => {
    e.preventDefault();
    const [clipX, clipY] = getClipSpaceMousePosition(e);
    // position before zooming
    const [preZoomX, preZoomY] = transformPoint(
        flatten(inverse3(viewProjectionMat)),
        [clipX, clipY]
    );

    // multiply the wheel movement by the current zoom level
    // so we zoom less when zoomed in and more when zoomed out
    const newZoom = camera.zoom * Math.pow(2, e.deltaY * -0.01);
    camera.zoom = Math.max(0.02, Math.min(1000000, newZoom));

    updateViewProjection();

    // position after zooming
    const [postZoomX, postZoomY] = transformPoint(
        flatten(inverse3(viewProjectionMat)),
        [clipX, clipY]
    );

    // camera needs to be moved the difference of before and after
    camera.x += preZoomX - postZoomX;
    camera.y += preZoomY - postZoomY;
    console.log(camera.zoom);

    render();
});

function render() {
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    let vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    escape_max = gl.getUniformLocation(program, "nt");
    gl.uniform1i(escape_max, nt);

    let matrix = gl.getUniformLocation(program, "matrix");
    gl.uniformMatrix3fv(matrix, false, [1, 0, 0, 0, 1, 0, 0, 0, 1]);

    let c_zoom = gl.getUniformLocation(program, "c_zoom");
    gl.uniform1f(c_zoom, camera.zoom);

    let c_x = gl.getUniformLocation(program, "c_x");
    gl.uniform1f(c_x, camera.x);

    let c_y = gl.getUniformLocation(program, "c_y");
    gl.uniform1f(c_y, camera.y);

    let c_r = gl.getUniformLocation(program, "c_r");
    gl.uniform1f(c_r, camera.rotation);

    let canvas_width = gl.getUniformLocation(program, "canvas_width");
    gl.uniform1f(canvas_width, gl.canvas.width);

    let canvas_height = gl.getUniformLocation(program, "canvas_height");
    gl.uniform1f(canvas_height, gl.canvas.height);

    updateViewProjection();

    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, vertices.length);
}
