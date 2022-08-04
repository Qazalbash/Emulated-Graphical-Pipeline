import numpy as np


class Primitive:

    def __init__(self, *vertices: np.ndarray) -> None:
        self.vertices = np.array(vertices)


class Point(Primitive):

    def __init__(self, *vertices) -> None:
        assert len(vertices) == 1, "Point must have one vertex"
        self.vertices = np.array(vertices)


class Line(Primitive):

    def __init__(self, *vertices) -> None:
        assert len(vertices) == 2, "Line must have two vertices"
        self.vertices = np.array(vertices)


class Triangle(Primitive):

    def __init__(self, *vertices) -> None:
        assert len(vertices) == 3, "Triangle must have three vertices"
        self.vertices = np.array(vertices)
