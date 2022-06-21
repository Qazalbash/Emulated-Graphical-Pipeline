import matplotlib.pyplot as plt

from vec import *

colors = []
points: list[vec] = []
numPoints = 5000
NumTimesToSubdivide = 4

vertices = [
    vec(0.0, 0.0, -1.0),
    vec(0.0, 0.9428, 0.3333),
    vec(-0.8165, -0.4714, 0.3333),
    vec(0.8165, -0.4714, 0.3333),
]


def triangle(a: vec, b: vec, c: vec) -> None:
    points.append(a)
    points.append(b)
    points.append(c)


def tetra(a: vec, b: vec, c: vec, d: vec) -> None:
    triangle(a, c, b)
    triangle(a, c, d)
    triangle(a, b, d)
    triangle(b, c, d)


def divideTetra(a: vec, b: vec, c: vec, d: vec, count: int) -> None:
    if count == 0:
        tetra(a, b, c, d)
    else:
        ab = scale(0.5, add(a, b))
        ac = scale(0.5, add(a, c))
        ad = scale(0.5, add(a, d))
        bc = scale(0.5, add(b, c))
        bd = scale(0.5, add(b, d))
        cd = scale(0.5, add(c, d))

        count -= 1

        divideTetra(a, ab, ac, ad, count)
        divideTetra(ab, b, bc, bd, count)
        divideTetra(ac, bc, c, cd, count)
        divideTetra(ad, bd, cd, d, count)


divideTetra(vertices[0], vertices[1], vertices[2], vertices[3],
            NumTimesToSubdivide)

x = [u.x for u in points]
y = [u.y for u in points]
z = [u.z for u in points]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x, y, z, color='black')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
