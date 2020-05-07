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


def hill_climbing(func, start_x, is_max):
    """
    find max/min using hill_climbing from the starting point
    """
    epsilon = 0.00001
    current_x = start_x

    def _best(_up, _down):
        """
        return the best, depending on is_max
        """

        if _up == _down:
            return None

        if is_max:
            # return the bigger
            if _up > _down:
                return _up
            return _down

        # return the bigger
        if _up < _down:
            return _up
        return _down

    while True:
        up = func(current_x + epsilon)
        current = func(current_x)
        down = func(current_x - epsilon)

        # we are at a peak, we are done
        if (_best(current, up) == current and
                _best(current, down) == current):
            return current_x

        best = _best(up, down)

        # we are stock a flat surface
        if best is None:
            return current_x

        if best == up:
            current_x += epsilon
        else:
            current_x -= epsilon
