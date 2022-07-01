"use strict";

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

	for (var i = -2; i <= 2; i += 1 / n) {
		for (var j = -2; j <= 2; j += 1 / n) {
			t = mandelbrot_set(vec2(i / n, j / n));
			level.push(t);
		}
	}

	console.log(level);
	drawScene();
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

function initBuffers() {
	// white
	// red
	// green
	// blue
	const colors = [
		1.0, 1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 0.0,
		1.0, 1.0,
	];

	const colorBuffer = gl.createBuffer();

	gl.bindBuffer(gl.ARRAY_BUFFER, colorBuffer);
	gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(colors), gl.STATIC_DRAW);

	return {
		position: positionBuffer,
		color: colorBuffer,
	};
}

function shaderProgram() {
	return level;
}

const vsSource = `
    attribute vec4 aVertexPosition;
    attribute vec4 aVertexColor;

    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;

    varying lowp vec4 vColor;

    void main(void) {
      gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
      vColor = aVertexColor;
    }
  `,
	fsSource = `
    varying lowp vec4 vColor;

    void main(void) {
      gl_FragColor = vColor;
    }
  `,
	programInfo = {
		program: shaderProgram,
		attribLocations: {
			vertexPosition: gl.getAttribLocation(
				shaderProgram,
				"aVertexPosition"
			),
			vertexColor: gl.getAttribLocation(shaderProgram, "aVertexColor"),
		},
	};
// Tell WebGL how to pull out the colors from the color buffer
// into the vertexColor attribute.
function drawScene() {
	var buffers = initBuffers();
	const numComponents = 4;
	const type = gl.FLOAT;
	const normalize = false;
	const stride = 0;
	const offset = 0;
	gl.bindBuffer(gl.ARRAY_BUFFER, buffers.color);
	gl.vertexAttribPointer(
		programInfo.attribLocations.vertexColor,
		numComponents,
		type,
		normalize,
		stride,
		offset
	);
	gl.enableVertexAttribArray(programInfo.attribLocations.vertexColor);
}
