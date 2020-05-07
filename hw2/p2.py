import copy
import random
import numpy as np

cards = list(range(1, 11))


class Individual:
    """
    A node in the space of the problem
    """

    def __init__(self, pile1, pile2):
        self.pile1 = copy.deepcopy(pile1)
        self.pile2 = copy.deepcopy(pile2)

    def is_valid(self):
        return (set(self.pile1) | set(self.pile2)) == set(cards)

    def rep(self):
        """
        represent the individual in 10 digits
        first 5 digits represent the first pile and
        second five digit represent the second pile
        each digit indicates what card is in that position
        """
        _rep = ""

        for digit in self.pile1:
            _rep += str(digit)

        for digit in self.pile2:
            _rep += str(digit)

        return _rep

    def utility(self):
        """
        Utility based on the difference
        of piles from perfect score
        """
        # perfect score 360 + (10 * 36)

        pile1_raw_score = abs(sum(self.pile1) - 36)
        pile1_score = 36 - pile1_raw_score

        pile2_raw_score = abs(sum(self.pile2) - 360)
        pile2_score = 360 - pile2_raw_score

        return pile2_score + 10 * pile1_score

    @staticmethod
    def form_rep(rep):
        """
        return a node from representation
        """

        pile1 = []
        pile2 = []

        for i in range(10):
            if i < 5:
                pile1.append(int(rep[i]))
            else:
                pile2.append(int(rep[i]))

        return Individual(pile1, pile2)

    def is_goal(self):
        """
        check if goal state
        """
        return sum(self.pile1) == 36 and np.prod(self.pile2) == 360

    @staticmethod
    def reproduce(father, mother):
        """
        Random reproduction
        """
        c = random.randint(0, 9)
        return Individual.form_rep(father.rep()[0:c] + mother.rep()[c:])

    @staticmethod
    def random_individual():
        """
        return a random individual
        """
        pile1 = random.sample(population=cards, k=5)
        pile2 = list(set(cards) - set(pile1))

        return Individual(pile1, pile2)

    def print_me(self):
        print("Pile 1: ", end='')
        for card in self.pile1:
            print(str(card) + "\t", end='')

        print("\nPile 2: ", end='')
        for card in self.pile2:
            print(str(card) + "\t", end='')

    def __eq__(self, other):
        return self.rep() == other.rep()


def genetic_solver():
    size_of_initial_population = 1000
    population = [Individual.random_individual() for i in range(size_of_initial_population)]

    while True:
        population_weights = [indv.utility() for indv in population]
        new_population = []

        for individual in population:

            if individual.is_goal():
                return individual

            father = np.random.choice(population, 1, population_weights)[0]
            mother = np.random.choice(population, 1, population_weights)[0]

            child = Individual.reproduce(father, mother)

            if child.is_valid():
                new_population.append(child)

        population = copy.deepcopy(new_population)


solution = genetic_solver()
solution.print_me()