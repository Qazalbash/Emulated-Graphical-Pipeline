from glcontext import *

gl = GLContext()

gl.set_canvas_size(800, 600)
gl.set_clear_color(0.0, 0.0, 0.0, 1.0)

gl.set_uniform("matrix", np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]]))
gl.set_attributes("position", np.array([[0.0, 0.5], [0.433, -0.5], [-0.433, -0.5]]))

gl.assembly_scheme = TRIANGLE

gl.set_attributes(
    "color",
    np.array([[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 1.0]]),
)

gl.set_count(3)


# dumy vertex shader
def vertex_shader(attribute: dict, uniform: dict) -> np.ndarray:
    matrix = uniform["matrix"]
    vertex = attribute["position"]
    for _ in range(3 - vertex.shape[0]):
        vertex = np.append(vertex, 0.0)
    vertex = np.transpose(np.append(np.matmul(matrix, vertex), 1.0))
    return vertex


# dumy fragment shader
def fragment_shader(attribute: dict, uniform: dict) -> np.ndarray:
    return 225 * attribute["color"]


gl.vShader = vertex_shader

gl.fShader = fragment_shader

gl.name = "tricolor-triangle.png"
