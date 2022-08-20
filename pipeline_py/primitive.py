from typing import Optional

import numpy as np


class Primitive:
    def __init__(self, *vertices: np.ndarray) -> None:
        pass

    def __iter__(self) -> np.ndarray:
        for vertex in self.vertices:
            yield vertex

    def __repr__(self) -> str:
        return str(self.vertices)


class Point(Primitive):
    def __init__(self, a: np.array | Optional[int | float], attributes: dict) -> None:
        self.vertices = a
        self.attributes = attributes


class Line(Primitive):
    def __init__(
        self,
        a: np.array | Optional[int | float],
        b: np.array | Optional[int | float],
        attributes: dict,
    ) -> None:
        self.vertices = np.array([a, b])
        self.attributes = attributes


class Triangle(Primitive):
    def __init__(
        self,
        a: np.array | Optional[int | float],
        b: np.array | Optional[int | float],
        c: np.array | Optional[int | float],
        attributes: dict,
    ) -> None:
        self.vertices = np.array([a, b, c])
        self.attributes = attributes


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

    def __repr__(self) -> str:
        # return "Vertex" + str(self.attributes["position"])
        return str(self.attributes)

    def __getitem__(self, index: int | slice) -> int | float | np.ndarray:
        if isinstance(index, slice):
            return self.attributes["position"][index.start : index.stop : index.step]
        elif isinstance(index, int):
            return self.attributes["position"][index]

    def __truediv__(self, divisor: int | float) -> np.ndarray:
        return self.attributes["position"] / divisor
