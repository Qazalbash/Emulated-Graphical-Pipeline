from app import *
from clipper import *
from vertex_processor import *

assert gl.count > 0, 'Number of rendering elements must be set in gl'

vp = Vertex_Processor(gl)
pos = vp.run_vertex_shader()

assert isinstance(
    pos, np.ndarray) and len(pos) == gl.count, 'Bad result from vertex shader'

gl.Position = pos

assert gl.assembly_scheme is not None, 'can not clip the vertices, assembly scheme is not defined.'

cpa = Clipper(gl)

gl.Position = cpa.run_clipper()
print(gl.Position)