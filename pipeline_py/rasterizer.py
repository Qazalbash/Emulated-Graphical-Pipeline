from glcontext import *


class Rasterizer:
    def __init__(self, gl: GLContext) -> None:
        self.gl = gl
        self.width = gl.width
        self.height = gl.height

    def gen_fragment(self, v: Vertex | np.ndarray) -> None:
        if isinstance(v, Vertex):
            v.fragment = np.array(
                [
                    (self.width * abs(v[0] + 1.0)) / 2.0,
                    (self.height * abs(v[1] - 1.0)) / 2.0,
                ],
                dtype=int,
            )
        elif isinstance(v, np.ndarray):
            for i in range(v.size):
                v[i].fragment = np.array(
                    [
                        (self.width * abs(v[i][0] + 1.0)) / 2.0,
                        (self.height * abs(v[i][1] - 1.0)) / 2.0,
                    ],
                    dtype=int,
                )

    def raster_points(self):
        np.vectorize(self.gen_fragment)(self.gl.Position)
        self.raster = self.gl.Position
        return self.raster

    def raster_lines(self) -> None:
        np.vectorize(self.gen_fragment)(self.gl.Position)
        positions = np.transpose(self.gl.Position)
        positions = np.vectorize(self.draw_line)(positions[0], positions[1])
        raster = np.array([], dtype=Vertex)
        for line in positions:
            raster = np.append(raster, line)
        return raster

    def raster_triangles(self) -> None:
        np.vectorize(self.gen_fragment)(self.gl.Position)
        positions = np.transpose(self.gl.Position)
        positions = np.vectorize(self.raster_traingle)(
            positions[0], positions[1], positions[2]
        )

        raster = np.array([], dtype=Vertex)
        for triangle in positions:
            raster = np.append(raster, triangle)
        return raster

    def raster_traingle(self, v0: Vertex, v1: Vertex, v2: Vertex) -> None:
        s01 = self.draw_line(v0, v1)
        s12 = self.draw_line(v1, v2)
        s20 = self.draw_line(v2, v0)

        border = np.append(s01, s12)
        border = np.append(border, s20)

        stack = {}

        for bVertex in border:
            height = bVertex.fragment[1]
            stack[height] = np.append(
                stack.get(height, np.array([], dtype=Vertex)), bVertex
            )

        raster = border

        for height in stack.keys():
            v0, v1 = sorted(stack[height], key=lambda v: v.fragment[1])[-2:]
            raster = np.append(raster, self.draw_line(v0, v1))

        return raster

    def run_rasterizer(self) -> np.ndarray:
        if self.gl.assembly_scheme == 1:  # POINT
            return self.raster_points()
        elif 1 < self.gl.assembly_scheme < 5:  # LINE
            return self.raster_lines()
        else:  # TRIANGLES
            return self.raster_triangles()

    @staticmethod
    def interpolate(v0: np.array, v1: np.array, size: float) -> np.array:
        return np.array(
            [(v0 * (size - index) + v1 * index) / size for index in range(size + 1)]
        )

    def interpolate_attributes(self, v0: Vertex, v1: Vertex, size: int):
        attr0 = v0.attributes.copy()
        attr1 = v1.attributes.copy()
        del attr0["fragment"]
        del attr1["fragment"]
        return {
            name: self.interpolate(attr0[name], attr1[name], size)
            for name in attr0.keys()
        }

    def draw_line(self, v0: Vertex, v1: Vertex) -> np.ndarray:

        x0, y0 = v0.fragment
        x0, y0 = int(x0), int(y0)
        x1, y1 = v1.fragment
        x1, y1 = int(x1), int(y1)

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

        line_frag = np.array([], dtype=int)

        for x in range(dx + 1):
            line_frag = np.append(
                line_frag, [x0 + x * xx + y * yx, y0 + x * xy + y * yy]
            )
            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy

        attr = self.interpolate_attributes(v0, v1, line_frag.size // 2)
        attr["fragment"] = line_frag.reshape(-1, 2)

        raster_line = np.array([], dtype=Vertex)

        for i in range(line_frag.size // 2):
            raster_line = np.append(
                raster_line, Vertex({k: v[i] for k, v in attr.items()})
            )
        return raster_line
