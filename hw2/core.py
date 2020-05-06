import matplotlib.pyplot as plt
import math


def f(x):
    """
    function of the question
    """
    return math.sin(10 * math.pi * x) / 2 * x + math.pow(x - 1, 4)


class Annotation:
    def __init__(self, text, x):
        self.text = text
        self.x = x


def plot_func(func, x_min, x_max, annotation=None):
    points = 1000  # Number of points
    step = (x_max - x_min) / points

    x_list = [(x_min + i * step) for i in range(points)]
    y_list = [func(x) for x in x_list]

    plt.plot(x_list, y_list)
    if annotation:
        plt.annotate(s=annotation.text, xy=(annotation.x, func(annotation.x)))
    plt.show()


plot_func(f, 0.5, 2.5, Annotation("hi", 1))
