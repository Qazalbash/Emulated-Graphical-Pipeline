from glcontext import *


class Rasterizer:

    def __init__(self, gl: GLContext) -> None:
        self.gl = gl

    def run_rasterizer(self) -> np.ndarray:
        self.gl.frame_buffer = np.full((self.gl.width, self.gl.height, 4), 1.0)
        print(self.gl.frame_buffer)
        print(self.gl.frame_buffer.shape)
