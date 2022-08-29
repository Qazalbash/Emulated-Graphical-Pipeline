from glcontext import *

gl = GLContext()  # GL object

# setting the viewport and clear color
gl.set_canvas_size(512, 512)
gl.set_clear_color(0.0, 0.0, 0.0, 1.0)

# setting the vertices
gl.set_attributes(
    "position",
    np.array([[0.0, 0.5, 0.0], [0.5, -0.5, 0.0], [-0.5, -0.5, 0.0]]),
)

# setting the assembly scheme
gl.assembly_scheme = TRIANGLE

# setting the color of each vertex
gl.set_attributes(
    "color",
    np.array([[1.0, 0.0, 0.0, 1.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0,
                                                           1.0]]),
)

# setting the number of vertices we want to pass to the shader
gl.set_count(3)


# dumy vertex shader
def vertex_shader(attribute: dict, uniform: dict):
    return np.append(attribute["position"], 1.0)


# dumy fragment shader
def fragment_shader(attribute: dict, uniform: dict):
    return 225 * attribute["color"]


# setting the shaders
gl.vShader = vertex_shader
gl.fShader = fragment_shader

# name of the file
gl.name = "plank-triangle.png"
