import matplotlib.pyplot as plt
import math

def f(x):
    """
    function of the question
    """
    return math.sin(10*math.pi*x) / 2*x + math.pow(x-1, 4)

def plot_func(func, xmin, xmax):

    points = 1000   # Number of points
    step = (xmax - xmin) / points

    xlist = [(xmin + i*step) for i in range(points)]
    ylist = [func(x) for x in xlist]

    plt.plot(xlist, ylist)
    plt.show()


plot_func(f, 0.5, 2.5)