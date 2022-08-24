import numpy as np

from primitive import *

# assembly schemes
POINT = 1
LINE = 2
LINESTRIP = 3
LINELOOP = 4
TRIANGLE = 5
TRIANGLESTRIP = 6
TRIANGLEFAN = 7


class GLContext:
    """class that mimics the WebGL API"""

    def __init__(self) -> None:

        # clear color or default color of canvas on RGBA format with 8 bit per channel
        self.clear_color = np.array([0, 0, 0, 225], dtype=np.uint8)

        # shader programs
        self.vShader = None
        self.fShader = None

        # dictionary of attributes
        self.attributes = {}

        # dictionary of uniforms
        self.uniforms = {}

        # number of vertices
        self.count = 0

        # position of vertices
        self.Position = None

        # fragments
        self.fragment = None

        # point size for points
        self.PointSize = 1.0

        # assembly scheme
        self.assembly_scheme = None

        # width and height of canvas
        self.width = None
        self.height = None

        # object that stores the image data
        self.frame_buffer = None

        # name of the image file
        self.name = None

    def set_count(self, count: int) -> None:
        """setter for count

        Args:
            count (int): number of time to run the vertex shader
        """
        self.count = count

    def set_clear_color(
        self, red: np.int8, green: np.int8, blue: np.int8, alpha: np.int8
    ) -> None:
        """setter for clear color

        Args:
            red (np.int8): value for red channel as an 8 bit int
            green (np.int8): value for green channel as an 8 bit int
            blue (np.int8): value for blue channel as an 8 bit int
            alpha (np.int8): value for alpha channel as an 8 bit int
        """
        assert 0 <= red <= 225, "red channel must be in range [0, 225]"
        assert 0 <= green <= 225, "green channel must be in range [0, 225]"
        assert 0 <= blue <= 225, "blue channel must be in range [0, 225]"
        assert 0 <= alpha <= 225, "alpha channel must be in range [0, 225]"
        self.clear_color = np.array([red, green, blue, alpha], dtype=np.uint8)

    def set_attributes(self, name: str, data: np.ndarray) -> None:
        """setter for attributes

        Args:
            name (str): name of the attribute
            data (np.ndarray): values of that attribute for each vertex in order
        """
        assert type(name) is str, "name of the attribute should be str type"
        assert type(data) is np.ndarray, "type of the data should be numpy array"
        self.attributes[name] = data

    def set_uniform(self, name: str, data: int | float | np.ndarray) -> None:
        """setter for uniforms

        Args:
            name (str): name of the uniform
            data (int | float | np.ndarray): value of the uniform
        """
        assert type(name) is str, "name of the attribute should be str type"
        assert (
            type(data) is int or type(data) is float or type(data) is np.ndarray
        ), "type of the data should be numpy array"
        self.uniforms[name] = data

    def set_canvas_size(self, width: int, height: int) -> None:
        """setter for canvas size

        Args:
            width (int): width of the canvas
            height (int): height of the canvas
        """
        self.width = width
        self.height = height
