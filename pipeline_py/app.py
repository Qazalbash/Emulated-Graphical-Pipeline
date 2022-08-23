from array import array
from glcontext import *

gl = GLContext()

gl.set_canvas_size(512, 512)
gl.set_clear_color(0.0, 0.0, 0.0, 1.0)


gl.set_attributes(
    "position",
    np.array([[0.0, 0.5, 0.0], [0.5, -0.5, 0.0], [-0.5, -0.5, 0.0]]),
)

gl.assembly_scheme = TRIANGLE

gl.set_attributes(
    "color",
    np.array([[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 1.0]]),
)

gl.set_count(3)


# dumy vertex shader
def vertex_shader(attribute: dict, uniform: dict):
    return np.append(attribute["position"], 1.0)


# dumy fragment shader
def fragment_shader(attribute: dict, uniform: dict):
    return 225 * attribute["color"]


gl.vShader = vertex_shader


gl.fShader = fragment_shader


gl.name = "plank-triangle.png"
