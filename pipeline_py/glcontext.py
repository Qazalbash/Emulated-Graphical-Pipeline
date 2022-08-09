import numpy as np

from primitive import *


class GLContext:

    def __init__(self) -> None:
        self.clearColor = (0.0, 0.0, 0.0, 1.0)
        self.vShader = None
        self.fShader = None
        self.attributes = {}
        self.uniforms = {}
        self.count = 0
        self.Position = None
        self.PointSize = 1.0
        self.assembly_scheme = None

    def set_count(self, count: int) -> None:
        self.count = count

    def set_clear_color(self, red: float, green: float, blue: float,
                        alpha: float) -> None:
        assert 0.0 <= red <= 1.0, "red channel must be in range [0.0, 1.0]"
        assert 0.0 <= green <= 1.0, "green channel must be in range [0.0, 1.0]"
        assert 0.0 <= blue <= 1.0, "blue channel must be in range [0.0, 1.0]"
        assert 0.0 <= alpha <= 1.0, "alpha channel must be in range [0.0, 1.0]"
        self.clearColor = (red, green, blue, alpha)

    def set_attributes(self, name: str, data: np.ndarray) -> None:
        self.attributes[name] = data

    def set_uniform(self, name: str, data: int | float | np.ndarray) -> None:
        self.uniforms[name] = data
