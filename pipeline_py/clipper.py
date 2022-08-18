from glcontext import GLContext
from primitive import *


class Clipper:

    def __init__(self, gl: GLContext):
        self.gl = gl

    @staticmethod
    def assemble_points(positions: np.ndarray) -> np.ndarray:
        return np.apply_along_axis(lambda x: Point(x), 1, positions)

    @staticmethod
    def assemble_lines(positions: np.ndarray, count: int) -> np.ndarray:
        # needs to implement line assembly
        positions = positions.reshape(-1, 3, 2)
        return np.apply_along_axis(lambda x: Line(x[0], x[1]), 1, positions)
        index = 0
        primitives = []
        while index + 1 < count:
            v0 = positions[index]
            v1 = positions[index + 1]
            index += 2
            primitives.append(Line(v0, v1))
        return primitives

    @staticmethod
    def assemble_linestrips(positions: np.ndarray, count: int) -> np.ndarray:
        index = 0
        primitives = []
        while index + 1 < count:
            v0 = positions[index]
            index += 1
            v1 = positions[index]
            primitives.append(Line(v0, v1))

    def run_clipper(self):

        weightened_positions = np.apply_along_axis(lambda x: x[:3] / x[3], 1,
                                                   self.gl.Position)

        positions = weightened_positions[
            -1.0 <= np.any(weightened_positions) <= 1.0].reshape(-1, 3)

        primitives = []

        count = self.gl.count
        index = 0

        if not (0 < self.gl.assembly_scheme.value < 8):
            raise TypeError("Invalid assembly scheme")

        elif self.gl.assembly_scheme.value == 1:  # points
            return self.assemble_points(positions)

        elif self.gl.assembly_scheme.value == 2:  # lines
            return self.assemble_lines(positions, self.gl.count)

        elif self.gl.assembly_scheme.value == 3:  # linestrip

            while index + 1 < count:

                v0 = self.gl.Position[index]

                index += 1

                v1 = self.gl.Position[index]

                v0 = v0[:3] / v0[3]
                v1 = v1[:3] / v1[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(v1) <= 1.0:
                    primitives.append(Line(v0, v1))

        elif self.gl.assembly_scheme.value == 4:  # lineloop

            while index + 1 < count:

                v0 = self.gl.Position[index]

                index += 1

                v1 = self.gl.Position[index]

                v0 = v0[:3] / v0[3]
                v1 = v1[:3] / v1[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(v1) <= 1.0:
                    primitives.append(Line(v0, v1))

            v0 = self.gl.Position[-1]
            v1 = self.gl.Position[0]

            v0 = v0[:3] / v0[3]
            v1 = v1[:3] / v1[3]

            if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(v1) <= 1.0:
                primitives.append(Line(v0, v1))

        elif self.gl.assembly_scheme.value == 5:  # triangles

            while index + 2 < count:

                v0 = self.gl.Position[index]
                v1 = self.gl.Position[index + 1]
                v2 = self.gl.Position[index + 2]

                index += 3

                v0 = v0[:3] / v0[3]
                v1 = v1[:3] / v1[3]
                v2 = v2[:3] / v2[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(
                        v1) <= 1.0 and -1.0 <= all(v2) <= 1.0:
                    primitives.append(Triangle(v0, v1, v2))

        elif self.gl.assembly_scheme.value == 6:  # triangle strip

            while index + 2 < count:

                v0 = self.gl.Position[index]

                index += 1

                v1 = self.gl.Position[index]
                v2 = self.gl.Position[index + 1]

                v0 = v0[:3] / v0[3]
                v1 = v1[:3] / v1[3]
                v2 = v2[:3] / v2[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(
                        v1) <= 1.0 and -1.0 <= all(v2) <= 1.0:
                    primitives.append(Triangle(v0, v1, v2))

        elif self.gl.assembly_scheme.value == 7:  # triangle fan

            v0 = self.gl.Position[0]
            v0 = v0[:3] / v0[3]
            index = 1
            while not (-1.0 <= all(v0) <= 1.0):
                v0 = self.gl.Position[index]
                v0 = v0[:3] / v0[3]
                index += 1

            while index + 1 < count:
                v1 = self.gl.Position[index]
                index += 1
                v2 = self.gl.Position[index]

                v1 = v1[:3] / v1[3]
                v2 = v2[:3] / v2[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(
                        v1) <= 1.0 and -1.0 <= all(v2) <= 1.0:
                    primitives.append(Triangle(v0, v1, v2))

        return primitives
