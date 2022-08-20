from glcontext import *
from PIL import Image


class Fragment_Processor:
    def __init__(self, gl: GLContext) -> None:
        self.gl = gl
        self.width = gl.width
        self.height = gl.height
        self.image = np.zeros((self.height, self.width, 4), dtype=np.uint8)

    def run_fragment_shader(self) -> np.ndarray:
        self.image[0 : self.height, 0 : self.width] = 225 * self.gl.clear_color

        for index in range(self.gl.count):
            frag_attr = self.gl.fragment[index].attributes
            shaded_frag = self.gl.fShader(frag_attr, self.gl.uniforms)
            assert isinstance(
                shaded_frag, np.ndarray
            ), "shader is not returning ndarray"
            assert shaded_frag.shape == (4,), "shader is not returning 4d vector"
            self.image[
                frag_attr["fragment"][1] - 1, frag_attr["fragment"][0] - 1
            ] = shaded_frag

        self.image = Image.fromarray(self.image, "RGBA")
        self.image.show()

    def save_image(self, name, path) -> None:
        pass
