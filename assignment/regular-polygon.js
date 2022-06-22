"use strict";

var gl, points;

window.onload = function init() {
	var canvas = document.getElementById("n-regular-polygon");
	gl = WebGLUtils.setupWebGL(canvas);

	if (!gl) {
		alert("WebGL is not available");
	}
	gl.viewport(0, 0, canvas.width, canvas.height);

	show();
};

function show() {
	var n = Number(document.getElementById("sides").value),
		color = document.getElementById("color").value;
	const theta = (2 * Math.PI) / n,
		r = 0.5;

	var x = r,
		y = 0;

	points = [vec2(r, 0)];

	for (var t = 1; t < n; t++) {
		x = r * Math.cos(theta * t);
		y = r * Math.sin(theta * t);
		points.push(vec2(x, y));
	}

	gl.clearColor(0.0, 0.0, 0.0, 1.0);

	var fshader = fragmentShader(color),
		vshader = vertexShader(),
		program = createProgram(gl, vshader, fshader);

	gl.useProgram(program);

	var vBuffer = gl.createBuffer();
	gl.bindBuffer(gl.ARRAY_BUFFER, vBuffer);
	gl.bufferData(gl.ARRAY_BUFFER, flatten(points), gl.STATIC_DRAW);

	var vPosition = gl.getAttribLocation(program, "vPosition");
	gl.vertexAttribPointer(vPosition, 2, gl.FLOAT, false, 0, 0);
	gl.enableVertexAttribArray(vPosition);

	render();
}

function fragmentShader(color) {
	var value = "1.0, 0.0, 0.0";

	if (color == "yellow") {
		value = "1.0, 1.0, 0.0";
	} else if (color == "green") {
		value = "0.0, 1.0, 0.0";
	} else if (color == "blue") {
		value = "0.0, 0.0, 1.0";
	} else if (color == "white") {
		value = "1.0, 1.0, 1.0";
	}

	var shader =
		"precision mediump float;\nvoid\nmain()\n{\ngl_FragColor = vec4( " +
		value +
		", 1.0 );\n}";

	return shader;
}

function vertexShader() {
	var shader =
		"attribute vec4 vPosition;\n" +
		"void\n" +
		"main()\n{\n" +
		"gl_PointSize = 1.0;\ngl_Position = vPosition;\n}\n";
	return shader;
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
	gl.drawArrays(gl.TRIANGLE_FAN, 0, points.length);
}
