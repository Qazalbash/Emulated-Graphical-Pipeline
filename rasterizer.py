from glcontext import *


class Rasterizer:
    """class for Rasterization"""

    def __init__(self, gl: GLContext) -> None:
        """Constructor for Vertex_Processor

        Args:
            gl (GLContext): WebGL context object
        """
        self.gl = gl
        # canvas width and height
        self.width = gl.width
        self.height = gl.height

    def gen_fragment(self, v: Vertex | np.ndarray) -> None:
        """generate fragment for each vertex

        Args:
            v (Vertex | np.ndarray): vertex object or array of vertex objects
        """
        frag = lambda v: np.array([(self.width * abs(v[0] + 1.0)) / 2.0,
                                   (self.height * abs(v[1] - 1.0)) / 2.0],
                                  dtype=int)
        # if vertex object is passed in as argument
        if isinstance(v, Vertex):
            # converting to fragments
            v.fragment = frag(v)
        # if array of vertex objects is passed in as argument
        elif isinstance(v, np.ndarray):
            for v_ in v:
                # converting to fragments
                v_.fragment = frag(v_)

    def raster_points(self) -> np.ndarray:
        """rasterize points

        Returns:
            np.ndarray: array of vertex objects
        """
        # rasterize points
        return self.gl.Position

    def raster_lines(self) -> np.ndarray:
        """rasterize lines

        Returns:
            np.ndarray: array of vertex objects
        """
        positions = np.transpose(self.gl.Position)
        # rasterize lines
        positions = np.vectorize(self.draw_line)(positions[0], positions[1])
        # flattening the array
        raster = np.array([], dtype=Vertex)
        for line in positions:
            raster = np.append(raster, line)
        return raster

    def raster_triangles(self) -> np.ndarray:
        """rasterize triangles

        Returns:
            np.ndarray: array of vertex objects
        """

        positions = np.transpose(self.gl.Position)
        # rasterize triangles
        positions = np.vectorize(self.draw_traingle)(positions[0],
                                                     positions[1],
                                                     positions[2])
        # flattening the array
        raster = np.array([], dtype=Vertex)
        for triangle in positions:
            raster = np.append(raster, triangle)
        return raster

    def draw_traingle(self, v0: Vertex, v1: Vertex, v2: Vertex) -> np.ndarray:
        # sides of the triangle
        s01 = self.draw_line(v0, v1)
        s12 = self.draw_line(v1, v2)
        s20 = self.draw_line(v2, v0)

        # border of the triangle
        border = np.append(s01, s12)
        border = np.append(border, s20)

        # stacking the vertices according to their height
        stack = {}
        for bVertex in border:
            height = bVertex.fragment[1]
            stack[height] = np.append(
                stack.get(height, np.array([], dtype=Vertex)), bVertex)

        # sorting the vertices according to their height
        # and then rasterizing the triangle
        raster = border
        for height in stack.keys():
            v0, v1 = sorted(stack[height], key=lambda v: v.fragment[1])[-2:]
            raster = np.append(raster, self.draw_line(v0, v1))
        return raster

    def run_rasterizer(self) -> np.ndarray:
        """run rasterizer

        Returns:
            np.ndarray: array of vertex objects
        """
        # generate fragments for each vertex
        np.vectorize(self.gen_fragment)(self.gl.Position)
        if self.gl.assembly_scheme == 1:  # POINT
            return self.raster_points()
        elif 1 < self.gl.assembly_scheme < 5:  # LINE
            return self.raster_lines()
        else:  # TRIANGLES
            return self.raster_triangles()

    @staticmethod
    def interpolate(v0: np.array, v1: np.array, size: int) -> np.ndarray:
        """interpolate between two values

        Args:
            v0 (np.array): first value
            v1 (np.array): second value
            size (int): size of the interpolation

        Returns:
            np.ndarray: interpolated values
        """
        return np.array([
            v0 * (1 - index / size) + v1 * (index / size)
            for index in range(size + 1)
        ])

    def interpolate_attributes(self, v0: Vertex, v1: Vertex,
                               size: int) -> dict:
        """interpolate between two vertex attributes

        Args:
            v0 (Vertex): first vertex
            v1 (Vertex): second vertex
            size (int): size of the interpolation

        Returns:
            dict: interpolated vertex attributes
        """
        attr0 = v0.attributes.copy()
        attr1 = v1.attributes.copy()
        del attr0["fragment"]
        del attr1["fragment"]
        return {
            name: self.interpolate(attr0[name], attr1[name], size)
            for name in attr0.keys()
        }

    def draw_line(self, v0: Vertex, v1: Vertex) -> np.ndarray:
        """draw line between two vertices using Bresenham's algorithm

        Args:
            v0 (Vertex): first vertex
            v1 (Vertex): second vertex

        Returns:
            np.ndarray: rastered line
        """
        # coordinates of the line
        x0, y0 = v0.fragment
        x0, y0 = int(x0), int(y0)
        x1, y1 = v1.fragment
        x1, y1 = int(x1), int(y1)

        # step size
        dx = x1 - x0
        dy = y1 - y0

        # sign of the step size
        xsign = (dx > 0) - (dx <= 0)  # 1 if positive, -1 if negative
        ysign = (dy > 0) - (dy <= 0)  # 1 if positive, -1 if negative

        dx = abs(dx)
        dy = abs(dy)

        if dx > dy:
            # horizontal line
            xx, xy, yx, yy = xsign, 0, 0, ysign
        else:
            # vertical line or 45 degree line
            dx, dy = dy, dx
            xx, xy, yx, yy = 0, ysign, xsign, 0

        D = 2 * dy - dx  # initial error
        y = 0  # initial y

        line_frag = np.array([], dtype=int)  # array with line fragments

        for x in range(dx + 1):
            # adding the vertex to the line
            line_frag = np.append(line_frag,
                                  [x0 + x * xx + y * yx, y0 + x * xy + y * yy])

            if D >= 0:
                y += 1
                D -= 2 * dx
            D += 2 * dy

        # interpolate attributes
        attr = self.interpolate_attributes(v0, v1, line_frag.size // 2)
        # add fragment to attributes
        attr["fragment"] = line_frag.reshape(-1, 2)
        # raster line
        raster_line = np.array([], dtype=Vertex)

        for i in range(line_frag.size // 2):
            # adding the vertex to the line
            raster_line = np.append(raster_line,
                                    Vertex({k: v[i]
                                            for k, v in attr.items()}))
        return raster_line
