import numpy as np


class Vertex_Processor:

    def __init__(self, glcontext, vertices: dict, vShader) -> None:
        self.glcontext = glcontext
        self.vertices = vertices['array']
        self.size = vertices['size']
        self.normalize = vertices['normalize']
        self.vShader = vShader
        self.transformed_vertices = self.run_vertex_shader()

    def run_vertex_shader(self) -> np.ndarray:
        transformed_vertices = []
        for index in range(0, len(self.vertices), self.size):
            transformed_vertices.append(
                self.vShader(self.glcontext,
                             self.vertices[index:index + self.size]))
        return np.array(transformed_vertices)
