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

    def __init__(self, a: np.array | Optional[int | float]) -> None:
        self.vertices = a


class Line(Primitive):

    def __init__(self, a: np.array | Optional[int | float],
                 b: np.array | Optional[int | float]) -> None:
        self.vertices = np.array([a, b])


class Triangle(Primitive):

    def __init__(self, a: np.array | Optional[int | float],
                 b: np.array | Optional[int | float],
                 c: np.array | Optional[int | float]) -> None:
        self.vertices = np.array([a, b, c])
