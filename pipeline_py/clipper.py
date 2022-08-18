from glcontext import GLContext
from primitive import *


class Clipper:

    def __init__(self, gl: GLContext):
        self.gl = gl

    def run_clipper(self):

        primitives = []

        count = self.gl.count
        index = 0

        if not (0 < self.gl.assembly_scheme.value < 8):
            raise TypeError("Invalid assembly scheme")

        elif self.gl.assembly_scheme.value == 1:  # points

            while index < count:
                v = self.gl.Position[index]

                index += 1

                v = v[:3] / v[3]

                if -1.0 <= all(v) <= 1.0:
                    primitives.append(Point(v))

        elif self.gl.assembly_scheme.value == 2:  # lines

            while index + 1 < count:

                v0 = self.gl.Position[index]
                v1 = self.gl.Position[index + 1]

                index += 2

                v0 = v0[:3] / v0[3]
                v1 = v1[:3] / v1[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(v1) <= 1.0:
                    primitives.append(Line(v0, v1))

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

            while index < count:

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
            while -1.0 <= all(v0) <= 1.0:
                v0 = self.gl.Position[index]
                v0 = v0[:3] / v0[3]
                index += 1

            while index < count:
                v1 = self.gl.Position[index]
                index += 1
                v2 = self.gl.Position[index]

                v1 = v1[:3] / v1[3]
                v2 = v2[:3] / v2[3]

                if -1.0 <= all(v0) <= 1.0 and -1.0 <= all(
                        v1) <= 1.0 and -1.0 <= all(v2) <= 1.0:
                    primitives.append(Triangle(v0, v1, v2))

        return primitives
