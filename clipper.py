from glcontext import GLContext
from primitive import *


class Clipper:
    """class for Clipping and Primitive Assembly"""

    def __init__(self, gl: GLContext):
        """Constructor for Vertex_Processor

        Args:
            gl (GLContext): WebGL context object
        """
        self.gl = gl

    @staticmethod
    def assemble_points(positions: np.ndarray) -> np.ndarray:
        """assembles points from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled points
        """
        # there is no need for assembling points
        # because they were inside the viewing volume
        return positions

    @staticmethod
    def assemble_lines(positions: np.ndarray) -> np.ndarray:
        """assembles lines from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled lines
        """

        if positions.size % 2:  # if the number of vertices is odd
            positions = positions[:-1]  # remove the last vertex
        return positions.reshape(-1, 2)  # reshape to 2D

    def assemble_linestrips(self, positions: np.ndarray) -> np.ndarray:
        """assembles linestrips from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled linestrips
        """
        # assembling lines pairing starts from first vertex
        line1 = self.assemble_lines(positions)
        # assembling lines pairing starts from second vertex
        line2 = self.assemble_lines(positions[1:])
        # merging both pairs to form a strip
        return np.append(line1, line2, axis=0)

    def assemble_lineloop(self, positions: np.ndarray) -> np.ndarray:
        """assembles lineloop from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled lineloop
        """
        # assembling the line strip
        strip = self.assemble_linestrips(positions)
        # adding a line from last vertex to first vertex
        strip = np.append(strip, [positions[-1], positions[0]])
        # reshaping to 2D
        return strip.reshape(-1, 2)

    @staticmethod
    def assemble_triangles(positions: np.ndarray) -> np.ndarray:
        """assembles triangles from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled triangles
        """
        if positions.size < 3:  # if the number of vertices is less than 3
            return np.array([])  # return an empty array
        elif positions.size % 3 == 1:  # if there is one extra vertex
            positions = positions[:-1]  # remove the last vertex
        elif positions.size % 3 == 2:  # if there are two extra vertices
            positions = positions[:-2]  # remove the last two vertices
        return positions.reshape(-1, 3)  # reshape to 2D

    def assemble_trianglestrip(self, positions: np.ndarray) -> np.ndarray:
        """assembles triangle strip from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled triangle strip
        """
        # assembling triangles from first vertx
        triangle1 = self.assemble_triangles(positions)
        # assembling triangles from second vertex
        triangle2 = self.assemble_triangles(positions[1:])
        # assembling triangles from third vertex
        triangle3 = self.assemble_triangles(positions[2:])
        # merging all triangles to form a strip
        triangle1 = np.append(triangle1, triangle2, axis=0)
        return np.append(triangle1, triangle3, axis=0)

    @staticmethod
    def assemble_trianglefan(positions: np.ndarray) -> np.ndarray:
        """assembles triangle fan from positions

        Args:
            positions (np.ndarray): positions of the vertices

        Returns:
            np.ndarray: assembled triangle fan
        """
        if positions.size < 3:  # if the number of vertices is less than 3
            return np.array([])  # return an empty array

        pivot = positions[0]  # get the first vertex as the pivot

        positions1 = positions[1:-1]  # get the rest of the vertices
        positions2 = positions[2:]  # get the rest of the vertices

        # merge the two arrays
        positions = np.append(positions1, positions2, axis=0).reshape(-1, 2)

        # add the pivot to the beginning of the array
        return np.apply_along_axis(lambda x: np.append(pivot, x), 1, positions)

    @staticmethod
    def viewing_filter(v: Vertex) -> bool:
        """filters vertices for visibility or bounding/viewing volume

        Args:
            v (Vertex): vertex to be filtered

        Returns:
            bool: True if visible, False if not
        """
        unit_v = v / v[3]  # normalize the vertex
        # if the vertex is inside the viewing volume
        if (-1.0 <= unit_v[0] <= 1.0 and -1.0 <= unit_v[1] <= 1.0
                and -1.0 <= unit_v[2] <= 1.0):
            v.position = unit_v  # update the vertex position
            return True  # return True because it is visible
        return False  # return False because it is not visible

    def run_clipper(self) -> np.ndarray:
        """runs the clipper

        Returns:
            np.ndarray: assembled primitive
        """

        # applying the viewing filter at all vertices at once
        mask = np.vectorize(self.viewing_filter)(self.gl.Position)

        # getting only vertices that are filtered
        positions = self.gl.Position[mask]

        # getting the primitive type that works only
        assert 0 < self.gl.assembly_scheme < 8, "Invalid assembly scheme"

        # assembling the primitive
        if self.gl.assembly_scheme == 1:  # points
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

        # if the primitive is empty then don't go further
        assert positions is not None, "No positions found for assembly"

        # trim the fourth component of the vertices
        np.vectorize(lambda v: v.trim())(positions)

        return positions  # return the assembled primitive
