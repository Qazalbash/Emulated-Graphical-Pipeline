from glcontext import *


class Fragment_Processor:
    """class for Fragment Processor"""

    def __init__(self, gl: GLContext) -> None:
        """Constructor for Vertex_Processor

        Args:
            gl (GLContext): WebGL context object
        """
        self.gl = gl
        self.width = gl.width
        self.height = gl.height
        self.frame_buffer = np.zeros((self.height, self.width, 4),
                                     dtype=np.uint8)

    def run_fragment_shader(self) -> np.ndarray:
        """it will run the fragment shader and return the result

        Returns:
            np.ndarray: colored fragments
        """
        # initiallizing frame buffer with clear color
        self.frame_buffer[0:self.height,
                          0:self.width] = 225 * self.gl.clear_color

        for index in range(self.gl.count):
            # attributes of the vertex at index i
            frag_attr = self.gl.fragment[index].attributes
            # running the fragment shader
            shaded_frag = self.gl.fShader(frag_attr, self.gl.uniforms)
            # if shader is returning the colored fragments
            assert isinstance(shaded_frag,
                              np.ndarray), "shader is not returning ndarray"
            # if shader is returning the colored fragments of the correct shape
            assert shaded_frag.shape == (
                4, ), "shader is not returning 4d vector"

            # storing the colored fragments in the frame buffer
            self.frame_buffer[frag_attr["fragment"][1] - 1,
                              frag_attr["fragment"][0] - 1] = shaded_frag

        return self.frame_buffer
