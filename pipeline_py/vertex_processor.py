from glcontext import *
from primitive import Vertex


class Vertex_Processor:
    """class for vertex processor"""

    def __init__(self, gl: GLContext) -> None:
        """Constructor for Vertex_Processor

        Args:
            gl (GLContext): WebGL context object
        """
        self.gl = gl

    def get_attributes(self, index: int) -> dict:
        """gets attribute of each vertex

        Args:
            index (int): index of the vertex

        Returns:
            dict: attributes of the vertex
        """
        return {
            attribute_name: attribute_value[index, :]
            for attribute_name, attribute_value in self.gl.attributes.items()
        }

    def run_vertex_shader(self) -> np.ndarray:
        """it will run the vertex shader and return the result

        Returns:
            np.ndarray: transformed vertices
        """
        # empty array to store the result
        positions = np.empty((self.gl.count, ), dtype=Vertex)

        for i in range(self.gl.count):

            # attributes of the vertex at index i
            attr = self.get_attributes(i)

            # running the vertex shader
            pos = self.gl.vShader(attr, self.gl.uniforms)

            # if shader is returning the transformed vertices
            assert isinstance(pos,
                              np.ndarray), "shader is not returning ndarray"

            # if shader is returning the transformed vertices of the correct shape
            assert pos.shape == (4, ), "shader is not returning 4d vector"

            # if shader is returning the transformed vertices with non-zero weight
            assert (
                pos[3] !=
                0.0), "Floating point error, 0.0 can not be assigned as weight"

            # reassigning the transformed vertex into the attribute dictonary
            attr["position"] = pos

            # adding the transformed vertex to the result array as Vertex object
            positions[i] = Vertex(attr)

        # returning the transformed vertices
        return positions
