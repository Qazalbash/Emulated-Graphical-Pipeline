"use strict";

var gl,
	t,
	level = [],
	n = 5;

window.onload = function init() {
	var canvas = document.getElementById("set");
	gl = WebGLUtils.setupWebGL(canvas);

	if (!gl) {
		alert("WebGL is not available");
	}

	gl.viewport(0, 0, canvas.width, canvas.height);
	for (var i = -2; i <= 2; i++) {
		for (var j = -2; j <= 2; j++) {
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
	return count;
}

const vSHADER = `attribute vec2 pos;
	varying vec2 _pos;
	
	void main() {
		gl_Position = vec4(_pos = pos, 0, 1);
	}`,
	fSHADER = `precision highp float;
	varying vec2 _pos;

	void main() {
	    vec2 c = _pos * 1.5 - vec2(0.7, 0), z;
	    for(int i = 0; i < 10000; i++) {
	        z = vec2(z.x * z.x - z.y * z.y, 2.0 * z.x * z.y) + c;
	        gl_FragColor = vec4(vec3((float(i) - log(log(length(z)))) / 64.0), 1);
	        if (length(z) > 2.0) return;
	    }
	    gl_FragColor = vec4(vec3(0), 1);`;

function draw() {
	gl.clearColor(0.0, 0.0, 0.0, 1.0);

	program = createProgram(gl, vSHADER, fSHADER);

	gl.useProgram(program);

	// gl.vertexAttribPointer(
	// 	gl.getAttribLocation(program, "pos"),
	// 	2,
	// 	gl.FLOAT,
	// 	false,
	// 	0,
	// 	0
	// );
	// gl.drawArrays(gl.TRIANGLES, 0, 6);

	var vBuffer = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
	gl.bufferData(gl.ARRAY_BUFFER, flatten(points), gl.STATIC_DRAW);

	var vPosition = gl.getAttribLocation(program, "pos");
	gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(vPosition);

	render();
}

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

function render() {
	gl.clear(gl.COLOR_BUFFER_BIT);
	gl.drawArrays(gl.TRIANGLE, 0, level.length);
}
