from glcontext import *

gl = GLContext()

gl.set_clear_color(1.0, 1.0, 1.0, 1.0)

N = 1000

# gl.set_uniform("matrix", np.random.rand(3, 3))
gl.set_uniform("matrix", np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]))

# gl.set_attributes("position", np.array([np.random.rand(2, 1) - 0.5 for _ in range(N)]))


lst = [
    [1, 1],
    [0.5, 0.5],
    [-1, 0.4],
    [1, -1],
    [-1, -1],
    [-0.3, 1],
]

N = len(lst)

# gl.set_attributes("color", np.array([np.random.rand(4, 4) for _ in range(N)]))

gl.assembly_scheme = Scheme.TRIANGLEFAN

gl.set_attributes("position", np.array(lst))

gl.set_count(N)

gl.set_canvas_size(800, 600)


# dumy vertex shader
def vertex_shader(attribute: dict, uniform: dict) -> np.ndarray:
    matrix = uniform["matrix"]
    vertex = attribute["position"]
    for _ in range(3 - vertex.shape[0]):
        vertex = np.append(vertex, 0.0)
    vertex = np.append(np.matmul(matrix, vertex), 1.0)
    return vertex


gl.vShader = vertex_shader
