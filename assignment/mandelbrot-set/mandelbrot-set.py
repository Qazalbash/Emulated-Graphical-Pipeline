import numpy as np
from matplotlib import pyplot as plt


def mandelbrot(c: complex, max_iterations=100):
    z = 0
    n = 0
    while max_iterations > n and abs(z) <= 2:
        z = z**2 + c
        n += 1
    return n


# plot mandelbrot set in python
def plot_mandelbrot(x_min, x_max, y_min, y_max, max_iterations=100):
    step = 0.005
    x_values = np.arange(x_min, x_max, step)
    y_values = np.arange(y_min, y_max, step)
    ms = [(x, y, mandelbrot(complex(x, y), max_iterations)) for x in x_values
          for y in y_values]
    plt.tight_layout()
    plt.scatter([i[0] for i in ms], [i[1] for i in ms], c=[i[2] for i in ms])
    plt.show()


plot_mandelbrot(-2, 2, -2, 2)
