from glcontext import *


class Rasterizer:

    def __init__(self, gl: GLContext) -> None:
        self.gl = gl

    def run_rasterizer(self) -> np.ndarray:
        width, height = self.gl.width, self.gl.height
        fragments = self.gl.Position + np.array([1.0, -1.0, 0.0], dtype=float)
        fragments = np.abs(
            np.array([width / 2.0, height / 2.0, 1.0]) * fragments)
        return fragments
