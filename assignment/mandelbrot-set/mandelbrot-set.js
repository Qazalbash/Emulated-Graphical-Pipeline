"use strict";

var gl,
	t,
	level = [(2, 1), (1, 1), (1, 2), (2, 2)],
	n = 10;

window.onload = function init() {
	var canvas = document.getElementById("set");
	gl = WebGLUtils.setupWebGL(canvas);

	if (!gl) {
		alert("WebGL is not available");
	}

	gl.viewport(0, 0, canvas.width, canvas.height);
	var z;
	for (var i = -2; i <= 2; i = i + 1 / n) {
		for (var j = -2; j <= 2; j = j + 1 / n) {
			level.push(mandelbrot_set(vec2(i, j)));
		}
	}

	draw();
};

function square(z) {
	// (a + bi)^2 = a^2 - b^2 + 2abi
	return vec2(z[0] * z[0] - z[1] * z[1], 2 * z[0] * z[1]);
}

function norm(z) {
	return Math.sqrt(z[0] ** 2 + z[1] ** 2);
}

function mandelbrot_set(c, MAX_ITTER = 100) {
	var count = 0,
		z = vec2(0.0, 0.0);
	while (norm(z) <= 2 && count <= MAX_ITTER) {
		z = add(square(z), c);
		count++;
	}
	if (norm(z) > 2) {
		return vec2(c);
	} else {
		return vec2(0.0, 0.0);
	}
}

var vSHADER = `attribute vec2 pos;
	varying vec2 _pos;
	
	void main() {
		gl_Position = vec4(_pos = pos, 0.0, 1.0);
	}`,
	fSHADER = `precision highp float;
	varying vec2 _pos;

	void main() {
		gl_FragColor = vec4(_pos, 1.0, 0.0);
	}`;

function createProgram(gl, vertexShaderSource, fragmentShaderSource) {
	var vsh = gl.createShader(gl.VERTEX_SHADER);
	gl.shaderSource(vsh, vertexShaderSource);
	gl.compileShader(vsh);
	if (!gl.getShaderParameter(vsh, gl.COMPILE_STATUS)) {
		throw "Error in vertex shader:  " + gl.getShaderInfoLog(vsh);
	}
	var fsh = gl.createShader(gl.FRAGMENT_SHADER);
	gl.shaderSource(fsh, fragmentShaderSource);
	gl.compileShader(fsh);
	if (!gl.getShaderParameter(fsh, gl.COMPILE_STATUS)) {
		throw "Error in fragment shader:  " + gl.getShaderInfoLog(fsh);
	}
	var prog = gl.createProgram();
	gl.attachShader(prog, vsh);
	gl.attachShader(prog, fsh);
	gl.linkProgram(prog);
	if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) {
		throw "Link error in program:  " + gl.getProgramInfoLog(prog);
	}
	return prog;
}

function draw() {
	gl.clearColor(0.0, 0.0, 0.0, 1.0);

	gl.useProgram(program);

	console.log(level);

	var program = createProgram(gl, vSHADER, fSHADER);

	var vBuffer = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
	gl.bufferData(gl.ARRAY_BUFFER, flatten(level), gl.STATIC_DRAW);

	var vPosition = gl.getAttribLocation(program, "pos");
	gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(vPosition);

	render();
}

function render() {
	gl.clear(gl.COLOR_BUFFER_BIT);
	gl.drawArrays(gl.TRIANGLE, 0, level.length);
}
