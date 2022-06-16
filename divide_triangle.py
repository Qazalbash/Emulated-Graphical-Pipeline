from vec import *
from matplotlib import pyplot as plt

points = []


def triangle(a: vec, b: vec, c: vec):
    points.append(a)
    points.append(b)
    points.append(c)


def divideTriangle(a: vec, b: vec, c: vec, count: int):
    if count == 0:
        triangle(a, b, c)
    else:
        ab = scale(0.5, add(a, b))
        bc = scale(0.5, add(b, c))
        ac = scale(0.5, add(a, c))

        count -= 1

        divideTriangle(a, ab, ac, count)
        divideTriangle(c, ac, bc, count)
        divideTriangle(b, bc, ab, count)


numTimesToSubdivide = 7
vertices = [vec(-1.0, -1.0), vec(0.0, 1.0), vec(1.0, -1.0)]

divideTriangle(vertices[0], vertices[1], vertices[2], numTimesToSubdivide)

x = [p.x for p in points]
y = [p.y for p in points]

plt.scatter(x, y, marker='.', color='black')
plt.tight_layout()
plt.show()