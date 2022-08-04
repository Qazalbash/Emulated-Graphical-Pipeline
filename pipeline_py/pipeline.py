from app import *
from vertex_processor import *

assert gl.count > 0, f'Number of rendering elements must be set in gl'
gl.Position = [None] * gl.count

vp = Vertex_Processor(gl)
pos = vp.run_vertex_shader()

assert isinstance(pos, np.ndarray) and len(pos) == gl.count,\
    'Bad result from vertex shader'

gl.Position = pos

print(gl.Position)
