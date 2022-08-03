import numpy as np


class GLContext:

    def __init__(self) -> None:
        self.clearColor = (0.0, 0.0, 0.0, 1.0)
        self.vShader = None
        self.fShader = None
        self.attribute = {}
        self.uniform = {}

    def set_clear_color(self, red: float, green: float, blue: float,
                        alpha: float) -> None:
        if (0.0 <= red <= 1.0 and 0.0 <= green <= 1.0 and 0.0 <= blue <= 1.0
                and 0.0 <= alpha <= 1.0):
            self.clearColor = (red, green, blue, alpha)
        else:
            raise ValueError("Invalid color values")

    def flatten(self, attrib: str) -> np.ndarray:
        return np.reshape(attrib, (-1, ))

    def set_vertices(self, name: str, data: np.ndarray, **extra) -> None:
        self.attribute[name] = {"data": data}
        for key in extra:
            self.attribute[name][key] = extra[key]

    def set_uniform(self, name: str, data: int | float | np.ndarray) -> None:
        self.uniform[name] = data
