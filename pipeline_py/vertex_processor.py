import numpy as np


class Vertex_Processor:

    def __init__(self, vShader, attribute: dict, uniform: dict) -> None:
        self.attribute = attribute
        self.uniform = uniform
        self.vShader = vShader
        self.transformed_vertices = self.run_vertex_shader()

    def run_vertex_shader(self) -> np.ndarray:
        transformed_vertices = np.array([])
        vertices = self.attribute["position"]["data"]

        for vertex in vertices:
            transformed_vertex = self.vShader(vertex, self.attribute,
                                              self.uniform)
            transformed_vertices = np.append(transformed_vertices,
                                             transformed_vertex)
        return transformed_vertices.reshape((3, -1))
