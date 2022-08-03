from glcontext import *

from vertex_processor import *

import numpy.linalg as la  # if you want to use matrix operations then this is the library you need to use

gl = GLContext()

gl.set_clear_color(1.0, 1.0, 1.0, 1.0)

gl.set_uniform("matrix", np.array([[2.0, 0.0, 0.0], [0.0, 2.0, 0.0], [0.0, 0.0, 2.0]]))

gl.set_vertices("position", np.array([0.0, 0.0, 1.0, 0.0, 0.0, 1.0]), 2)

gl.attribute["color"] = {
    "data": gl.flatten(
        np.array([0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0, 0.0])
    ),
    "size": 4,
}


def vertex_shader(vertex, attribute: dict, uniform: dict) -> np.ndarray:
    matrix = uniform["matrix"]
    if vertex.shape[0] < 3:
        for _ in range(3 - vertex.shape[0]):
            vertex = np.append(vertex, 0.0)
    return np.matmul(matrix, vertex)


gl.vShader = vertex_shader

vp = Vertex_Processor(gl.vShader, {"attribute": gl.attribute, "uniform": gl.uniform})

print(vp.transformed_vertices)
