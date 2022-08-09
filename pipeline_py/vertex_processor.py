from glcontext import *


class Vertex_Processor:

    def __init__(self, gl: GLContext) -> None:
        self.gl = gl

    def get_attributes(self, index: int):
        return {
            attribute_name: attribute_value[index, :]
            for attribute_name, attribute_value in self.gl.attributes.items()
        }

    def run_vertex_shader(self) -> np.ndarray:
        positions = np.empty((self.gl.count, 4), dtype=np.ndarray)
        for index in range(self.gl.count):
            pos = self.gl.vShader(self.get_attributes(index), self.gl.uniforms)
            assert isinstance(pos,
                              np.ndarray), "shader is not returning ndarray"
            assert pos.shape == (4, ), "shader is not returning 4d vector"
            assert pos[
                3] != 0.0, "Floating point error, 0.0 can not be assigned as weight"
            positions[index] = pos
        return positions
