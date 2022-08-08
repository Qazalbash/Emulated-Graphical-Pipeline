import math
import random

from matplotlib import pyplot as plt

from vec import *

numPoints = 5000

vertices = [
    vec(-1.0, -1.0),
    vec(0.0, 1.0),
    vec(1.0, -1.0),
]

u = scale(0.5, add(vertices[0], vertices[1]))
v = scale(0.5, add(vertices[0], vertices[2]))
p = scale(0.5, add(u, v))

points = [p]

for i in range(1, numPoints):
    j = math.floor(random.random() * 3)
    p = scale(0.5, add(points[i - 1], vertices[j]))
    points.append(p)

x = [u.x for u in points]
y = [u.y for u in points]

plt.title = f'SIERPINSKI GASKET as generated with {numPoints} random points'
plt.scatter(x, y, marker='.', color='black')
plt.tight_layout()
plt.show()
