from glcontext import *


class Fragment_Processor:

    def __init__(self, gl: GLContext, shader, varying: dict,
                 uniform: dict) -> None:
        self.gl = gl
        self.shader = shader
        self.varying = varying
        self.uniform = uniform

    def run_fragment_shader(self) -> np.ndarray:
        pass
