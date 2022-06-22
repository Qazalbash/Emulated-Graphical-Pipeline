"use strict";

var gl,
	points = [],
	z,
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
			z = point_gen(vec2(0.0, 0.0), vec2(i / n, j / n));
			points.push(z);
		}
	}

	console.log(points);
};

function square(z) {
	// (a + bi)^2 = a^2 - b^2 + 2abi
	return vec2(z[0] * z[0] - z[1] * z[1], 2 * z[0] * z[1]);
}

function norm(z) {
	return Math.sqrt(z[0] ** 2 + z[1] ** 2);
}

function point_gen(z, c, generation = 10) {
	if (norm(z) <= 2) {
		if (generation == 0) {
			return z;
		}
		generation--;
		z = add(square(z), c);
		return point_gen(z, c, generation);
	}
	return vec2(0.0, 0.0);
}
