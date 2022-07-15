"use strict";

var gl,
	level = [];

const MAX_ITERATION = 100;

window.onload = function init() {
	var canvas = document.getElementById("set");
	gl = WebGLUtils.setupWebGL(canvas);

	if (!gl) {
		alert("WebGL is not available");
	}
	gl.clearColor(1.0, 1.0, 1.0, 1.0);

	var program = createProgram(gl, vSHADER, fSHADER);
	gl.useProgram(program);

	const real = { start: -2, end: 2 },
		imag = { start: -2, end: 2 };
	let colors = [],
		width = canvas.width,
		height = canvas.height;
	var color,
		complex,
		red = vec4(0.8, 0, 0, 1),
		green = vec4(0, 1, 0, 1),
		blue = vec4(0, 0, 1, 1);

	for (let p = 0; p <= width; p++) {
		for (let q = 0; q <= height; q++) {
			complex = {
				x: map_point(
					vec2(0, 0),
					vec2(width, 0),
					vec2(real.start, 0),
					vec2(real.end, 0),
					vec2(p, 0)
				)[0],
				y: map_point(
					vec2(0, 0),
					vec2(0, height),
					vec2(0, imag.start),
					vec2(0, imag.end),
					vec2(0, q)
				)[1],
			};
			const escapetime = mandelbrot_set(complex);
			let new_complex = {
				nx: map_point(
					vec2(real.start, 0),
					vec2(real.end, 0),
					vec2(-1, 0),
					vec2(1, 0),
					vec2(complex.x, 0)
				)[0],
				ny: map_point(
					vec2(0, imag.start),
					vec2(0, imag.end),
					vec2(0, -1),
					vec2(0, 1),
					vec2(0, complex.y)
				)[1],
			};

			level.push(vec2(new_complex.nx, new_complex.ny));

			if (escapetime == MAX_ITERATION) {
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

function square(z) {
	// (a + bi)^2 = a^2 - b^2 + 2abi
	return vec2(z[0] * z[0] - z[1] * z[1], 2 * z[0] * z[1]);
}

function norm(z) {
	return Math.sqrt(z[0] ** 2 + z[1] ** 2);
}

function mandelbrot_set(c) {
	c = vec2(c.x, c.y);
	var count = 0,
		z = vec2(0.0, 0.0);
	do {
		z = add(square(z), c);
		count++;
	} while (norm(z) <= 2 && count <= MAX_ITERATION);

	return count;
}

var vSHADER = `
			attribute vec2 vPosition;
			attribute vec4 vColor;
			varying vec4 g1_vColor;

			void main(){
				gl_Position = vec4(vPosition, 0.0, 1.0);
				g1_vColor = vColor;
				gl_PointSize = 1.0;
			}`,
	fSHADER = `
			precision highp float;
			uniform vec4 g1_vColor;
			// varying vec4 fragColor;
	
			void main()
			{
				gl_FragColor = g1_vColor;
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
function render() {
	gl.clear(gl.COLOR_BUFFER_BIT);
	gl.drawArrays(gl.POINTS, 0, level.length);
}

function map_point(P, Q, A, B, X) {
	/*
    This Function maps X from PQ to AB
    where 
    P, Q = Two points on a line segment
    X = affine combination of P, Q such that X = αQ + (1 − α)P such that |P X| : |XQ| = α : (1 − α) , 0 ≤ α ≤ 1
    A, B = colors at P, and Q respectively
    It returns Y which is the mapping of PQ to AB
    types:
    X, P, Q = vec2
    A, B, Y = vec4
    */
	var PX = 0;
	var PQ = 0;
	let PX_dist = 0;
	let PQ_dist = 0;
	// for (let i = 0; i < P.length; i++) {
	// 	PX += (P[i] - X[i]) ** 2; //calculates square to calculare distance

	// 	PQ += (P[i] - Q[i]) ** 2; //calculates square to calculare distance
	// }

	// PX_dist = Math.sqrt(PX); //distance between P and X
	// PQ_dist = Math.sqrt(PQ); //distance between P and Q

	// const alpha = PX_dist / PQ_dist;
	//checks if it's a vector
	// if (isVector(P)) {
	// 	for (let i = 0; i < P.length; i++) {
	// 		PX += (P[i] - X[i]) ** 2; //calculates square to calculare distance

	// 		PQ += (P[i] - Q[i]) ** 2; //calculates square to calculare distance
	// 	}

	// 	PX_dist = Math.sqrt(PX); //distance between P and X
	// 	PQ_dist = Math.sqrt(PQ); //distance between P and Q

	// 	alpha = PX_dist / PQ_dist;
	// } else {
	// 	//if it's not a point
	// 	PX_dist = X - P;
	// 	PQ_dist = Q - P;
	// 	alpha = PX_dist / PQ_dist;
	// }
	PX_dist = X - P;
	PQ_dist = Q - P;
	const alpha = PX_dist / PQ_dist;
	//mapped point on the given A B range
	let Y = mix(A, B, alpha);

	return Y;
}
