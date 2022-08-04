"use strict";

var gl,
    level = [];

const MAX_ITERATION = 100;

function norm(z) {
    return Math.sqrt(z.x * z.x + z.y * z.y);
}

const arg = function (z) {
    return Math.atan2(z.y, z.x);
};

function mandelbrot_set(c, n) {
    let count = 0,
        r = 0,
        t = 0,
        z = { x: 0.0, y: 0.0 };

    do {
        z.x = Math.pow(r, n) * Math.cos(n * t) + c.x;
        z.y = Math.pow(r, n) * Math.sin(n * t) + c.y;

        r = norm(z);
        t = arg(z);

        count++;
    } while (r <= 2 && count <= MAX_ITERATION);

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
    return v.type == "vec2" || v.type == "vec3" || v.type == "vec4";
}

window.onload = function init() {
    var canvas = document.getElementById("set");
    gl = WebGLUtils.setupWebGL(canvas);

    if (!gl) {
        alert("WebGL is not available");
    }

    gl.viewport(0, 0, canvas.width, canvas.height);

    draw(2, canvas.width, canvas.height);
};

function draw(n = 2, width = 512, height = 512) {
    const range = { start: -2, end: 2 };

    let colors = [];

    var color,
        z,
        red = vec4(1, 0, 0, 1),
        green = vec4(0, 1, 0, 1),
        blue = vec4(0, 0, 1, 1);

    gl.clearColor(0.0, 0.0, 0.0, 1.0);
    for (let p = 0; p <= width; p++) {
        for (let q = 0; q <= height; q++) {
            z = {
                x: map_point(0, width, range.start, range.end, p),
                y: map_point(0, height, range.start, range.end, q),
            };

            let z_ = {
                x: map_point(range.start, range.end, -1, 1, z.x),
                y: map_point(range.start, range.end, -1, 1, z.y),
            };

            level.push(vec2(z_.x, z_.y));

            const escapetime = mandelbrot_set(z, n);

            if (escapetime == MAX_ITERATION + 1) {
                color = blue;
            } else {
                color = map_point(0, MAX_ITERATION / 4, red, green, escapetime);
            }

            colors.push(color);
        }
    }

    var program = initShaders(gl, "vShader", "fShader");
    gl.useProgram(program);

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
}

function render() {
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.drawArrays(gl.POINTS, 0, level.length);
}

// const name = "Meesum";

// const show = function () {
//     const name = "Meesum Ali";

//     if (true) {
//         var _name = "Meesum Ali";
//         const name = "Meesum Ali Qazalbash";

//         console.log(name);
//     }

//     console.log(_name);
// };

// document.querySelector(".button", show);
