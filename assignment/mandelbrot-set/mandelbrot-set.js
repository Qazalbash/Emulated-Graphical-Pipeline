"use strict";

var gl,
	level = [];

const MAX_ITERATION = 100;

var vSHADER = `attribute vec2 vPosition;
			attribute vec4 vColor;
			varying vec4 colors;

			void main(){
				gl_Position = vec4(vPosition, 0.0, 1.0);
				colors = vColor;
				gl_PointSize = 1.0;
			}`,
	fSHADER = `precision highp float;
			varying vec4 colors;
	
			void main()
			{
				gl_FragColor = colors;
			}`;

function norm(z) {
	return Math.sqrt(z.x * z.x + z.y * z.y);
}

function mandelbrot_set(c) {
	let count = 0,
		z = { x: 0.0, y: 0.0 },
		z_ = { x: 0.0, y: 0.0 };
	do {
		z_.x = z.x * z.x - z.y * z.y + c.x;
		z_.y = 2 * z.x * z.y + c.y;
		z.x = z_.x;
		z.y = z_.y;
		count++;
	} while (norm(z) <= 2 && count <= MAX_ITERATION);

	return count;
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

function map_point(P, Q, A, B, X) {
	var PX_dist = X - P,
		PQ_dist = Q - P,
		alpha = PX_dist / PQ_dist;

	return mix(A, B, alpha);
}

function isVector(v) {
	if (v.type == "vec2" || v.type == "vec3" || v.type == "vec4") {
		return true;
	}
	return false;
}

window.onload = function init() {
	var canvas = document.getElementById("set");
	gl = WebGLUtils.setupWebGL(canvas);

	if (!gl) {
		alert("WebGL is not available");
	}

	gl.viewport(0, 0, canvas.width, canvas.height);
	gl.clearColor(1.0, 1.0, 1.0, 1.0);

	var program = createProgram(gl, vSHADER, fSHADER);
	gl.useProgram(program);

	const real = { start: -2, end: 2 },
		imag = { start: -2, end: 2 };

	let colors = [],
		width = canvas.width,
		height = canvas.height;

	var color,
		z,
		red = vec4(1, 0, 0, 1),
		green = vec4(0, 1, 0, 1),
		blue = vec4(0, 0, 1, 1);

	for (let p = 0; p <= width; p++) {
		for (let q = 0; q <= height; q++) {
			z = {
				x: map_point(0, width, real.start, real.end, p),
				y: map_point(0, height, imag.start, imag.end, q),
			};

			const escapetime = mandelbrot_set(z);

			let z_ = {
				x: map_point(real.start, real.end, -1, 1, z.x),
				y: map_point(imag.start, imag.end, -1, 1, z.y),
			};

			level.push(vec2(z_.x, z_.y));

			if (escapetime == MAX_ITERATION + 1) {
				color = blue;
			} else if (escapetime == 1) {
				color = red;
			} else {
				color = map_point(0, MAX_ITERATION / 4, red, green, escapetime);
			}
			colors.push(color);
		}
	}

	gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
	gl.bufferData(gl.ARRAY_BUFFER, flatten(level), gl.STATIC_DRAW);

	// // Associate out shader variables with our data buffer
	let vPosition = gl.getAttribLocation(program, "vPosition");
	gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(vPosition);
	// //colors
	gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
	gl.bufferData(gl.ARRAY_BUFFER, flatten(colors), gl.STATIC_DRAW);

	// // Associate out shader variables with our data buffer
	let vColorPosition = gl.getAttribLocation(program, "vColor");
	gl.vertexAttribPointer(vColorPosition, 4, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(vColorPosition);

	render();
};

function render() {
	gl.clear(gl.COLOR_BUFFER_BIT);
	gl.drawArrays(gl.POINTS, 0, level.length);
}
