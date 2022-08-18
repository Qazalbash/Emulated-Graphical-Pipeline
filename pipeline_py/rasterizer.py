from glcontext import *


class Rasterizer:
    def __init__(self, gl: GLContext) -> None:
        self.gl = gl

    def run_rasterizer(self) -> np.ndarray:
        width, height = self.gl.width, self.gl.height
        fragments = self.gl.Position + np.array([1.0, -1.0, 0.0], dtype=float)
        fragments = np.abs(np.array([width / 2.0, height / 2.0, 1.0]) * fragments)
        return fragments

    def raster_triangle(self, v1: np.array, v2: np.array, v3: np.array) -> None:
        pass

    @staticmethod
    def bressenham(v0: np.array, v1: np.array) -> np.ndarray:
        x0, y0, x1, y1 = v0[0], v0[1], v1[0], v1[1]

        dx = x1 - x0
        dy = y1 - y0

        xsign = (dx > 0) - (dx <= 0)  # 1 if positive, -1 if negative
        ysign = (dy > 0) - (dy <= 0)  # 1 if positive, -1 if negative

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2 * dy - dx
        y = 0

        line = []

        for x in range(dx + 1):
            line.append((x0 + x * xx + y * yx, y0 + x * xy + y * yy))
            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy
        return line
