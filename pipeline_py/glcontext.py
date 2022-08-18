import numpy as np

from primitive import *
import enum


class Scheme(enum.Enum):
    POINT = 1
    LINE = 2
    LINESTRIP = 3
    LINELOOP = 4
    TRIANGLE = 5
    TRIANGLESTRIP = 6
    TRIANGLEFAN = 7


class GLContext:

    def __init__(self) -> None:
        self.clear_color = np.array([0.0, 0.0, 0.0, 1.0], dtype=float)
        self.vShader = None
        self.fShader = None
        self.attributes = {}
        self.uniforms = {}
        self.count = 0
        self.Position = None
        self.PointSize = 1.0
        self.assembly_scheme = None
        self.zbuffer = None
        self.width = None
        self.height = None
        self.frame_buffer = None

    def set_count(self, count: int) -> None:
        self.count = count

    def set_clear_color(self, red: int | float, green: int | float,
                        blue: int | float, alpha: int | float) -> None:
        assert 0.0 <= red <= 1.0, "red channel must be in range [0.0, 1.0]"
        assert 0.0 <= green <= 1.0, "green channel must be in range [0.0, 1.0]"
        assert 0.0 <= blue <= 1.0, "blue channel must be in range [0.0, 1.0]"
        assert 0.0 <= alpha <= 1.0, "alpha channel must be in range [0.0, 1.0]"
        self.clear_color = (red, green, blue, alpha)

    def set_attributes(self, name: str, data: np.ndarray) -> None:
        assert type(name) is str, "name of the attribute should be str type"
        assert type(
            data) is np.ndarray, "type of the data should be numpy array"
        self.attributes[name] = data

    def set_uniform(self, name: str, data: int | float | np.ndarray) -> None:
        assert type(name) is str, "name of the attribute should be str type"
        assert type(data) is int or type(data) is float or type(
            data) is np.ndarray, "type of the data should be numpy array"
        self.uniforms[name] = data

    def set_canvas_size(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
