# to calculate the time spent in each stage of the pipeline
from time import time

# PIL will create the image
from PIL import Image

# importing the modules of application program and pipeline stages
from app import *
from clipper import *
from fragment_processor import *
from rasterizer import *
from vertex_processor import *

# rendering starts from here
start = time()

# checking it we have set the viewport, clear color and count of the vertices
assert gl.width is not None, "width of the canvas is not set"
assert gl.height is not None, "height of the canvas is not set"
assert gl.clear_color is not None, "clear color is not set"
assert gl.count is not None, "count of the vertices is not set"
assert gl.count > 0, "Number of rendering elements must be set in gl"

# running the vertex processor
vp = Vertex_Processor(gl)
gl.Position = vp.run_vertex_shader()

print("Vertex shader time:", time() - start)
start = time()

# checking if the assembly scheme is set
assert (
    gl.assembly_scheme
    is not None), "can not clip the vertices, assembly scheme is not defined."

# running the clipper
cpa = Clipper(gl)
gl.Position = cpa.run_clipper()

print("Clipper time:", time() - start)
start = time()

# running the rasterizer
ras = Rasterizer(gl)
gl.fragment = ras.run_rasterizer()
# resetting the count of the vertices
# because some vertices are clipped out and many new are added
gl.set_count(gl.fragment.size)

print("Rasterizer time:", time() - start)
start = time()

# running the fragment processor
fp = Fragment_Processor(gl)
frame_buffer = fp.run_fragment_shader()

print("Fragment shader time:", time() - start)
start = time()

# saving the image to the file
image = Image.fromarray(frame_buffer, "RGBA")
image.save("pipeline_py/output/" + gl.name)
image.show()
