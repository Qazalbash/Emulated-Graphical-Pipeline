import numpy as np


class Vertex:

    def __init__(self, attributes: dict) -> None:
        self.attributes = attributes

    @property
    def position(self) -> np.array:
        return self.attributes["position"]

    @position.setter
    def position(self, value: np.array) -> None:
        self.attributes["position"] = value

    @property
    def fragment(self) -> np.ndarray:
        return self.attributes.get("fragment", None)

    @fragment.setter
    def fragment(self, frag: np.ndarray) -> None:
        self.attributes["fragment"] = frag

    def trim(self) -> None:
        self.attributes["position"] = self.attributes["position"][:3]

    def __repr__(self) -> str:
        return "Vertex" + str(self.attributes["position"])

    def __getitem__(self, index: int | slice) -> int | float | np.ndarray:
        if isinstance(index, slice):
            return self.attributes["position"][index.start:index.stop:index.
                                               step]
        elif isinstance(index, int):
            return self.attributes["position"][index]

    def __truediv__(self, divisor: int | float) -> np.ndarray:
        return self.attributes["position"] / divisor
