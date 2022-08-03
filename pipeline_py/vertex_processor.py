import numpy as np


class Vertex_Processor:
    def __init__(self, vShader, attr: dict) -> None:
        self.attribute = attr["attribute"]
        self.uniform = attr["uniform"]
        self.vShader = vShader
        self.transformed_vertices = self.run_vertex_shader()

    def run_vertex_shader(self) -> np.ndarray:
        transformed_vertices = np.array([])
        vertices = self.attribute["position"]["data"]
        size = self.attribute["position"]["size"]

        for index in range(len(vertices) // size):
            transformed_vertex = self.vShader(
                vertices[index * size : (index + 1) * size],
                self.attribute,
                self.uniform,
            )
            transformed_vertices = np.append(transformed_vertices, transformed_vertex)

        return transformed_vertices
