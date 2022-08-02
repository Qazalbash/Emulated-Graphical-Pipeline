import numpy as np


class GLContext:

    def __init__(self) -> None:
        self.clearColor = (0.0, 0.0, 0.0, 1.0)
        self.vShader = None
        self.fShader = None
        self.uniform_value = {}
        self.attrib_value = {}
        self.keyword = {}

    def set_clear_color(self, red: float, green: float, blue: float,
                        alpha: float) -> None:
        if 0.0 <= red <= 1.0 and 0.0 <= green <= 1.0 and 0.0 <= blue <= 1.0 and 0.0 <= alpha <= 1.0:
            self.clearColor = (red, green, blue, alpha)
        else:
            raise ValueError("Invalid color values")

    def set_vertex_attribute(self, name: str, vertex_array: np.ndarray,
                             size: int, normalize: bool) -> None:
        self.attrib_value[name] = {
            "array": vertex_array,
            "size": size,
            "normalize": normalize
        }

    def set_uniform_value(self, uniform: str,
                          value: int | float | np.ndarray) -> None:
        self.uniform_value[uniform] = value

    def set_attrib_value(self, attrib: str,
                         value: int | float | np.ndarray) -> None:
        self.attrib_value[attrib] = value

    def get_uniform_value(self, uniform: str) -> int | float | np.ndarray:
        return self.uniform_value[uniform]

    def get_attrib_value(self, attrib: str) -> int | float | np.ndarray:
        return self.attrib_value[attrib]
