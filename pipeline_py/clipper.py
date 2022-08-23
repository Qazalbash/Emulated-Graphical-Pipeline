from glcontext import GLContext
from primitive import *


class Clipper:
    def __init__(self, gl: GLContext):
        self.gl = gl

    @staticmethod
    def assemble_points(positions: np.ndarray) -> np.ndarray:
        return positions

    @staticmethod
    def assemble_lines(positions: np.ndarray) -> np.ndarray:
        if positions.size % 2:
            positions = positions[:-1]
        positions = positions.reshape(-1, 2)
        return positions

    def assemble_linestrips(self, positions: np.ndarray) -> np.ndarray:
        line1 = self.assemble_lines(positions)
        line2 = self.assemble_lines(positions[1:])
        return np.append(line1, line2, axis=0)

    def assemble_lineloop(self, positions: np.ndarray) -> np.ndarray:
        strip = self.assemble_linestrips(positions)
        strip = np.append(strip, [positions[-1], positions[0]])
        return strip.reshape(-1, 2)

    @staticmethod
    def assemble_triangles(positions: np.ndarray) -> np.ndarray:
        if positions.size < 3:
            return np.array([])
        elif positions.size % 3 == 1:
            positions = positions[:-1]
        elif positions.size % 3 == 2:
            positions = positions[:-2]
        positions = positions.reshape(-1, 3)
        return positions

    def assemble_trianglestrip(self, positions: np.ndarray) -> np.ndarray:
        triangle1 = self.assemble_triangles(positions)
        triangle2 = self.assemble_triangles(positions[1:])
        triangle3 = self.assemble_triangles(positions[2:])

        triangle1 = np.append(triangle1, triangle2, axis=0)

        return np.append(triangle1, triangle3, axis=0)

    @staticmethod
    def assemble_trianglefan(positions: np.ndarray) -> np.ndarray:

        if positions.size < 3:
            return np.array([])

        pivot = positions[0]

        positions1 = positions[1:-1]
        positions2 = positions[2:]

        positions = np.append(positions1, positions2, axis=0).reshape(-1, 2)

        positions = np.apply_along_axis(
            lambda x: np.append(pivot, x),
            1,
            positions,
        )
        return positions

    @staticmethod
    def veiwing_filter(v: Vertex) -> bool:
        unit_v = v / v[3]
        if (
            -1.0 <= unit_v[0] <= 1.0
            and -1.0 <= unit_v[1] <= 1.0
            and -1.0 <= unit_v[2] <= 1.0
        ):
            v.position = unit_v
            return True
        return False

    def run_clipper(self):

        mask = np.vectorize(self.veiwing_filter)(self.gl.Position)

        positions = self.gl.Position[mask]

        if not (0 < self.gl.assembly_scheme < 8):
            raise TypeError("Invalid assembly scheme")

        elif self.gl.assembly_scheme == 1:  # points
            positions = self.assemble_points(positions)

        elif self.gl.assembly_scheme == 2:  # lines
            positions = self.assemble_lines(positions)

        elif self.gl.assembly_scheme == 3:  # linestrip
            positions = self.assemble_linestrips(positions)

        elif self.gl.assembly_scheme == 4:  # lineloop
            positions = self.assemble_lineloop(positions)

        elif self.gl.assembly_scheme == 5:  # triangles
            positions = self.assemble_triangles(positions)

        elif self.gl.assembly_scheme == 6:  # triangle strip
            positions = self.assemble_trianglestrip(positions)

        elif self.gl.assembly_scheme == 7:  # triangle fan
            positions = self.assemble_trianglefan(positions)

        np.vectorize(lambda v: v.trim())(positions)

        return positions
