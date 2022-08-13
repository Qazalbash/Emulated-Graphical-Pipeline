from glcontext import GLContext
from primitive import *


class Clipper:

    def __init__(self, gl: GLContext):
        self.gl = gl

    def run_clipper(self):
        clipped_pos = np.array(np.array([], dtype=float), dtype=np.ndarray)

        if self.gl.assembly_scheme == Point:
            for vertex in self.gl.Position:
                vertex = vertex[:3] / vertex[3]
                if -1.0 <= vertex[0] <= 1.0 and -1.0 <= vertex[
                        1] <= 1.0 and -1.0 <= vertex[2] <= 1.0:
                    clipped_pos = np.append(clipped_pos, vertex)

        elif self.gl.assembly_scheme == Line:
            raise NotImplementedError("Line clipper is not implemented yet")

        elif self.gl.assembly_scheme == Triangle:
            raise NotImplementedError(
                "Triangle clipper is not implemented yet")
        else:
            raise TypeError(f"{self.gl.assembly_scheme} is an invalid type")

        zbuffer = np.array(np.array([], dtype=float), dtype=np.ndarray)

        for z in range(0, len(clipped_pos), 3):
            vecz = np.full((1, 3), clipped_pos[z])
            normal_vecz = vecz / np.linalg.norm(vecz)
            zbuffer = np.append(zbuffer, normal_vecz)

        clipped_pos = clipped_pos.reshape(-1, 3)
        zbuffer = zbuffer.reshape(-1, 3)
        self.gl.zbuffer = zbuffer

        return clipped_pos
