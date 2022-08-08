"use strict";

let gl,
    vertices = [(-1.0, 1.0), (1.0, 1.0), (1.0, -1.0), (-1.0, -1.0)];
var program;

window.onload = function init() {
    var canvas = document.getElementById("set");
    gl = canvas.getContext("webgl2");

    if (!gl) {
        alert("WebGL 2.0 is not available");
    }

    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.clearColor(0.0, 0.0, 0.0, 1.0);

    program = initShaders(gl, "vShader", "fShader");
    gl.useProgram(program);

    // uncomment the code if you are calculating vertices on the CPU

    /*
    var vBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
    gl.bufferData(gl.ARRAY_BUFFER, flatten(
        // name of the array with that contain all the vertices
    ), gl.STATIC_DRAW);
    
    var vPosition = gl.getAttribLocation(program,
        "vPosition" // name of the attribute, by defualt it is "vPosition"
    );
    gl.vertexAttribPointer(vPosition,
        2, // number of components per vertex
        gl.FLOAT, // type
        false, // normalize
        0, // stride
        0 // offset
    );
    gl.enableVertexAttribArray(vPosition);
    */

    // uncomment the code if you are calculating color for each vertex on the CPU

    /*
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
	gl.bufferData(gl.ARRAY_BUFFER, flatten(
        // name of the array that contains all the colors
    ), gl.STATIC_DRAW);

	let vColorPosition = gl.getAttribLocation(program,
        "vColor" // name of the attribute, by defualt it is "vColor"
    );
	gl.vertexAttribPointer(vColorPosition,
        4, // number of components per vertex, it must 4 because WebGL uses RGBA
        gl.FLOAT, // type
        false, // normalize
        0, // stride
        0 // offset
        );
	gl.enableVertexAttribArray(vColorPosition);
    */

    render();
};

function render() {
    gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
    gl.bufferData(gl.ARRAY_BUFFER, flatten(vertices), gl.STATIC_DRAW);

    let vPosition = gl.getAttribLocation(program, "vPosition");
    gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
    gl.enableVertexAttribArray(vPosition);

    let world = gl.getUniformLocation(program, "worldMatrix");
    gl.uniformMatrix3fv(world, false, [1, 0, 0, 0, 1, 0, 0, 0, 1]);

    let view = gl.getUniformLocation(program, "viewMatrix");
    gl.uniformMatrix3fv(view, false, [1, 0, 0, 0, 1, 0, 0, 0, 1]);

    let projection = gl.getUniformLocation(program, "projectionMatrix");
    gl.uniformMatrix3fv(projection, false, [1, 0, 0, 0, 1, 0, 0, 0, 1]);

    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.TRIANGLE_FAN, 0, vertices.length);
}
