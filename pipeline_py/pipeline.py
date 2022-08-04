from app import *
from vertex_processor import *

vp = Vertex_Processor(gl, gl.vShader, gl.attribute, gl.uniform)

print(gl.transformed_vertices)
