import math
import random
import matplotlib.pyplot as plt


class vec3:

    def __init__(self, x: int | float, y: int | float, z: int | float) -> None:
        self.x = x
        self.y = y
        self.z = z


def add(u: vec3, v: vec3) -> vec3:
    return vec3(u.x + v.x, u.y + v.y, u.z + v.z)


def scale(factor: int | float, u: vec3) -> vec3:
    return vec3(u.x * factor, u.y * factor, u.z * factor)


numPoints = 5000

vertices = [vec3(-1.0, -1.0, 0.0), vec3(0.0, 1.0, 0.0), vec3(1.0, -1.0, 0.0)]

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
z = [u.z for u in points]

fig = plt.figure()
ax = plt.axes(projection='3d')
ax.scatter3D(x, y, z, color='black')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
