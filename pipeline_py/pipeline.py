from glcontext import *

from vertex_processor import *

gl = GLContext()

gl.uniform_value["matrix"] = np.array([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0],
                                       [0.0, 0.0, 1.0]])

gl.set_vertex_attribute("position", np.array([0.0, 0.0, 1.0, 0.0, 0.0, 1.0]),
                        2, False)


def vertex_shader(gl: GLContext, vertex):
    return vertex // 2


vp = Vertex_Processor(gl, gl.get_attrib_value("position"), vertex_shader)
