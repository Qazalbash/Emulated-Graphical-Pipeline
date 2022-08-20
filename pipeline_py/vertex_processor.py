from glcontext import *
from primitive import Vertex


class Vertex_Processor:
    def __init__(self, gl: GLContext) -> None:
        self.gl = gl

    def get_attributes(self, index: int):
        return {
            attribute_name: attribute_value[index, :]
            for attribute_name, attribute_value in self.gl.attributes.items()
        }

    def run_vertex_shader(self) -> np.ndarray:
        positions = np.empty((self.gl.count,), dtype=Vertex)
        for index in range(self.gl.count):
            attr = self.get_attributes(index)
            pos = self.gl.vShader(attr, self.gl.uniforms)
            assert isinstance(pos, np.ndarray), "shader is not returning ndarray"
            assert pos.shape == (4,), "shader is not returning 4d vector"
            assert (
                pos[3] != 0.0
            ), "Floating point error, 0.0 can not be assigned as weight"
            attr["position"] = pos
            positions[index] = Vertex(attr)
        return positions
