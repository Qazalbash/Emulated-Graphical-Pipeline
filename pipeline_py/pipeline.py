from glcontext import *

from vertex_processor import *

gl = GLContext()

gl.set_clear_color(1.0, 1.0, 1.0, 1.0)

gl.set_uniform("matrix",
               np.array([[2.0, 0.0, 0.0], [0.0, 2.0, 3.0], [1.0, 0.0, 2.0]]))

gl.set_vertices("position", np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]))

gl.attribute["color"] = {
    "data":
    np.array([[0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 1.0,
                                                           0.0]]),
    "size":
    4
}


def vertex_shader(vertex, attribute: dict, uniform: dict) -> np.ndarray:
    matrix = uniform["matrix"]
    for _ in range(3 - vertex.shape[0]):
        vertex = np.append(vertex, 0.0)
    return np.matmul(matrix, vertex)


gl.vShader = vertex_shader

vp = Vertex_Processor(gl.vShader, gl.attribute, gl.uniform)

print(vp.transformed_vertices)
