from app import *
from clipper import *
from fragment_processor import *
from rasterizer import *
from vertex_processor import *

assert gl.width is not None, "width of the canvas is not set"
assert gl.height is not None, "height of the canvas is not set"
assert gl.count > 0, "Number of rendering elements must be set in gl"

vp = Vertex_Processor(gl)
pos = vp.run_vertex_shader()

assert (
    isinstance(pos, np.ndarray) and len(pos) == gl.count
), "Bad result from vertex shader"

gl.Position = pos


assert (
    gl.assembly_scheme is not None
), "can not clip the vertices, assembly scheme is not defined."

cpa = Clipper(gl)

gl.Position = cpa.run_clipper()


# assert gl.zbuffer is not None, "zbuffer is not created, that could cause problem while rasterization"

ras = Rasterizer(gl)

gl.fragment = ras.run_rasterizer()

gl.set_count(gl.fragment.size)


fp = Fragment_Processor(gl)

fp.run_fragment_shader()
