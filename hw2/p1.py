"""
Problem 1
"""
import math
import random
import matplotlib.pyplot as plt
from core import plot_func, Annotation, hill_climbing

max_iterations = 1000  # total number of iterations
t_start = math.inf  # starting temperature
t_end = 0.00001  # ending temperature
reduction_factor = (t_end / t_start) ** (1 / max_iterations)


def f(x):
    """
    function of the question
    """
    return math.sin(10 * math.pi * x) / 2 * x + math.pow(x - 1, 4)


def p(delta_e, t):
    """
    probability of next move
    """

    return math.exp(- delta_e / t)


def iterative_hill_climbing(func, x_current, t, x_start, x_end):
    # choose random x and remove it from the list
    x_random = random.uniform(x_start, x_end)
    delta_e = func(x_random) - func(x_current)

    if delta_e < 0:
        # take the move
        return x_random

    # decide based on probability
    if p(delta_e, t) > 0:
        return x_random

    return x_current


def temperature(iteration):
    """
    temperature at the given iteration
    """
    return t_start * (reduction_factor ** iteration)


def simulated_annealing(func, x_start, x_end):
    x_current = x_start

    # generate an approximation of the solution
    for i in range(1, max_iterations):
        x_current = iterative_hill_climbing(func, x_current,
                                            temperature(i), x_start, x_end)

    # use hill climbing to generate accurate solution
    return hill_climbing(func, x_current, False)


def p1():
    """
    Problem 1, 1: Hill Climbing
    """
    solution = simulated_annealing(f, 0.5, 2.5)
    plot_func(f, 0.5, 2.5, Annotation("(%f,%f)" % (solution, f(solution)), solution))
    plt.show()


def test():
    print("Calculating Accuracy ...")
    number_of_tests = 100
    actual_solution = 1.5498
    correct = 0

    for i in range(number_of_tests):
        print('{0}/{1}'.format(i, number_of_tests), end='\r')
        solution = simulated_annealing(f, 0.5, 2.5)

        if math.fabs(solution - actual_solution) < 0.001:
            correct += 1

    print("Accuracy: %.2f percent" % (correct / number_of_tests * 100))


test()
p1()
