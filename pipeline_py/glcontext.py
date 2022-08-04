import numpy as np


class GLContext:

    def __init__(self) -> None:
        self.clearColor = (0.0, 0.0, 0.0, 1.0)
        self.vShader = None
        self.fShader = None
        self.attributes = {}
        self.uniform = {}
        self.count = 0
        self.Position = None
        self.PointSize = 1
        self.transformed_vertices = None
        # self.assembly_scheme = pass # TODO: look up enum for assembly schemes

    def set_count(self, count: int) -> None:
        self.count = count

    def set_clear_color(self, red: float, green: float, blue: float,
                        alpha: float) -> None:
        if (0.0 <= red <= 1.0 and 0.0 <= green <= 1.0 and 0.0 <= blue <= 1.0
                and 0.0 <= alpha <= 1.0):
            self.clearColor = (red, green, blue, alpha)
        else:
            raise ValueError("Invalid color values")

    def set_attributes(self, name: str, data: np.ndarray) -> None:
        self.attributes[name] = data

    def set_uniform(self, name: str, data: int | float | np.ndarray) -> None:
        self.uniform[name] = data
