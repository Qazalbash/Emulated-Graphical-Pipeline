import numpy as np


class Primitive:

    def __init__(self, *vertices: np.ndarray) -> None:
        self.vertices = np.ndarray(vertices)

    def __iter__(self) -> np.ndarray:
        for vertex in self.vertices:
            yield vertex


class Point(Primitive):

    def __init__(self, *vertices) -> None:
        assert len(vertices) == 1, "Point primitive only have one vertex"
        self.vertices = np.array(vertices)


class Line(Primitive):

    def __init__(self, *vertices) -> None:
        assert len(vertices) == 2, "Line primitive only have two vertices"
        self.vertices = np.array(vertices)


class Triangle(Primitive):

    def __init__(self, *vertices) -> None:
        assert len(
            vertices) == 3, "Triangle primitive only have three vertices"
        self.vertices = np.array(vertices)
