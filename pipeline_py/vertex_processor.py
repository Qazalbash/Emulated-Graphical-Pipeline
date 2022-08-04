from glcontext import *


class Vertex_Processor:

    def __init__(self, gl: GLContext, shader, attribute: dict,
                 uniform: dict) -> None:
        self.gl = gl
        self.attribute = attribute
        self.uniform = uniform
        self.shader = shader
        self.run_vertex_shader()

    def get_attributes(self, index: int):
        return {
            name: value[index, :]
            for name, value in self.attribute.items()
        }

    def run_vertex_shader(self) -> np.ndarray:
        t_vert = np.array([])
        vert = self.attribute["position"]

        for index in range(len(vert)):
            transformed_vertex = self.shader(self.get_attributes(index),
                                             self.uniform)
            t_vert = np.append(t_vert, transformed_vertex)

        self.gl.transformed_vertices = t_vert.reshape((3, -1))
