"""
Problem 1
"""
import math
import random
import matplotlib.pyplot as plt

from core import hill_climbing, plot_func, Annotation


def f(x):
    """
    function of the question
    """
    return math.sin(10 * math.pi * x) / 2 * x + math.pow(x - 1, 4)


def global_minima_hill_climbing(func, x_start, x_end):
    """
    global minima using hill climbing
    """
    attempts = 1000

    # initial value
    global_min_x = hill_climbing(func, random.uniform(x_start, x_end), False)

    for i in range(attempts):
        tmp_x = hill_climbing(func, random.uniform(x_start, x_end), False)

        # better minimum found
        if func(tmp_x) < func(global_min_x):
            global_min_x = tmp_x

    return global_min_x


def p1_1():
    """
    Problem 1, 1: Hill Climbing
    """
    plot_func(f, 0.5, 2.5, Annotation("Global Minima", global_minima_hill_climbing(f, 0.5, 2.5)))
    plt.show()

