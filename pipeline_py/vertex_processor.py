from glcontext import *


class Vertex_Processor:

    def __init__(self, gl: GLContext) -> None:
        self.gl = gl

    def get_attributes(self, index: int):
        return {
            name: value[index, :]
            for name, value in self.gl.attributes.items()
        }

    def run_vertex_shader(self) -> np.ndarray:
        positions = np.empty((self.gl.count, 4), dtype=np.ndarray)
        for index in range(self.gl.count):
            pos = self.gl.vShader(self.get_attributes(index), self.gl.uniform)
            assert isinstance(
                pos,
                np.ndarray) and len(pos) == 4, 'Bad result from vertex shader'
            positions[index] = pos
        return positions
