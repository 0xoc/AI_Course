import matplotlib.pyplot as plt


class Annotation:
    """
    Annotation on on the plotted function
    """

    def __init__(self, text, x):
        self.text = text
        self.x = x


def plot_func(func, x_min, x_max, annotation=None):
    """
    plot a function by generating discreet points on the function
    annotate the function if any given
    """
    points = 1000  # Number of points
    step = (x_max - x_min) / points

    x_list = [(x_min + i * step) for i in range(points)]
    y_list = [func(x) for x in x_list]

    plt.plot(x_list, y_list)
    if annotation:
        plt.annotate(s=annotation.text,
                     xy=(annotation.x, func(annotation.x)),
                     xytext=(annotation.x, 3),
                     arrowprops=dict(facecolor='black', shrink=0.05))
