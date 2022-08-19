from glcontext import GLContext
from primitive import *


class Clipper:
    def __init__(self, gl: GLContext):
        self.gl = gl

    @staticmethod
    def assemble_points(positions: np.ndarray) -> np.ndarray:
        return positions
        # return np.apply_along_axis(lambda x: Point(x), 1, positions)

    @staticmethod
    def assemble_lines(positions: np.ndarray) -> np.ndarray:
        if positions.size % 2:
            positions = positions[:-1]
        positions = positions.reshape(-1, 2, 3)
        return positions
        # return np.apply_along_axis(lambda x: x[:3], x[3:], 1, positions)

    def assemble_linestrips(self, positions: np.ndarray) -> np.ndarray:
        line1 = self.assemble_lines(positions)
        line2 = self.assemble_lines(positions[1:])
        return np.append(line1, line2, axis=0)

    def assemble_lineloop(self, positions: np.ndarray) -> np.ndarray:
        strip = self.assemble_linestrips(positions)
        strip = np.append(strip, [positions[-1], positions[0]])
        return strip.reshape(-1, 2, 3)

    @staticmethod
    def assemble_triangles(positions: np.ndarray) -> np.ndarray:
        if positions.size < 9:
            return np.array([])
        elif (positions.size / 3) % 3 == 1:
            positions = positions[:-1]
        elif (positions.size / 3) % 3 == 2:
            positions = positions[:-2]
        positions = positions.reshape(-1, 3, 3)
        return positions
        # return np.apply_along_axis(
        #     lambda x: Triangle(x[:3], x[3:6], x[6:]), 1, positions
        # )

    def assemble_trianglestrip(self, positions: np.ndarray) -> np.ndarray:
        triangle1 = self.assemble_triangles(positions)
        triangle2 = self.assemble_triangles(positions[1:])
        triangle3 = self.assemble_triangles(positions[2:])

        triangle1 = np.append(triangle1, triangle2, axis=0)

        return np.append(triangle1, triangle3, axis=0)

    @staticmethod
    def assemble_trianglefan(positions: np.ndarray) -> np.ndarray:

        if positions.size < 9:
            return np.array([])

        pivot = np.transpose(positions[0])

        positions1 = positions[1:-1]
        positions2 = positions[2:]
        positions = np.append(positions1, positions2, axis=1)
        positions = np.apply_along_axis(lambda x: np.append(x, pivot), 1, positions)
        return positions.reshape(-1, 3, 3)

        # return np.apply_along_axis(
        #     lambda x: Triangle(pivot, x[:3], x[3:]), 1, positions
        # )

    def run_clipper(self):

        weightened_positions = np.apply_along_axis(
            lambda x: x[:3] / x[3], 1, self.gl.Position
        )

        positions = weightened_positions[
            -1.0 <= np.any(weightened_positions) <= 1.0
        ].reshape(-1, 3)

        if not (0 < self.gl.assembly_scheme.value < 8):
            raise TypeError("Invalid assembly scheme")

        elif self.gl.assembly_scheme.value == 1:  # points
            return self.assemble_points(positions)

        elif self.gl.assembly_scheme.value == 2:  # lines
            return self.assemble_lines(positions)

        elif self.gl.assembly_scheme.value == 3:  # linestrip
            return self.assemble_linestrips(positions)

        elif self.gl.assembly_scheme.value == 4:  # lineloop
            return self.assemble_lineloop(positions)

        elif self.gl.assembly_scheme.value == 5:  # triangles
            return self.assemble_triangles(positions)

        elif self.gl.assembly_scheme.value == 6:  # triangle strip
            return self.assemble_trianglestrip(positions)

        elif self.gl.assembly_scheme.value == 7:  # triangle fan
            return self.assemble_trianglefan(positions)
