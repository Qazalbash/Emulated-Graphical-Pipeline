from glcontext import *

gl = GLContext()

gl.set_clear_color(1.0, 1.0, 1.0, 1.0)

gl.set_uniform("matrix", np.array([[2.0, 0.0, 0.0], [0.0, 2.0, 3.0], [1.0, 0.0, 2.0]]))

gl.set_vertices("position", np.array([[0.0, 0.0], [1.0, 0.0], [0.0, 1.0]]))

gl.attribute["color"] = np.array(
    [
        [0.0, 0.0, 1.0, 0.0],
        [0.0, 1.0, 0.0, 0.0],
        [1.0, 0.0, 1.0, 0.0],
    ]
)

# dumy vertex shader
def vertex_shader(attribute: dict, uniform: dict) -> np.ndarray:
    matrix = uniform["matrix"]
    vertex = attribute["position"]
    for _ in range(3 - vertex.shape[0]):
        vertex = np.append(vertex, 0.0)
    return np.matmul(matrix, vertex)


gl.vShader = vertex_shader
