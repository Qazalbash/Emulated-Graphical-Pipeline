from glcontext import *

gl = GLContext()

gl.set_clear_color(1.0, 1.0, 1.0, 1.0)

N = 1000

gl.set_uniform("matrix", np.random.rand(3, 3))

gl.set_attributes("position",
                  np.array([np.random.rand(3, 1) for _ in range(N)]))

gl.set_attributes("color", np.array([np.random.rand(4, 4) for _ in range(N)]))

gl.set_count(N)


# dumy vertex shader
def vertex_shader(attribute: dict, uniform: dict) -> np.ndarray:
    matrix = uniform["matrix"]
    vertex = attribute["position"]
    for _ in range(3 - vertex.shape[0]):
        vertex = np.append(vertex, 0.0)
    vertex = np.append(np.matmul(matrix, vertex), 1.0)
    return vertex


gl.vShader = vertex_shader
gl.assembly_scheme = Point
