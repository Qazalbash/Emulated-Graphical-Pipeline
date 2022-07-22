"use strict";

var gl, vertices;

const MAX_ITERATION = 100;

window.onload = function init() {
    var canvas = document.getElementById("set");
    gl = canvas.getContext("webgl2");

    if (!gl) {
        alert("WebGL2.0 is not available");
    }

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    var program = initShaders(gl, "vShader", "fShader");
    gl.useProgram(program);

    vertices = [
        vec2(-1.0, 1.0),
        vec2(1.0, 1.0),
        vec2(1.0, -1.0),
        vec2(-1.0, -1.0),
    ];

    render();
};

function render() {
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    // // Associate out shader variables with our data buffer
    let vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    excape_max = gl.getUniformLocation(program, "MAX_ITERATION");
    gl.uniform1f(excape_max, MAX_ITERATION);

    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, vertices.length);
}
