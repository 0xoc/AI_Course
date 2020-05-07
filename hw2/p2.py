import copy
import random
import numpy as np
import matplotlib.pyplot as plt

cards = list(range(1, 11))


class Individual:
    """
    A node in the space of the problem
    """

    def __init__(self, pile1, pile2):
        self.pile1 = copy.deepcopy(pile1)
        self.pile2 = copy.deepcopy(pile2)

    def sort_piles(self):
        """
        Sort piles, sorting yields better reproduction results
        """
        self.pile1.sort()
        self.pile2.sort()

    def is_valid(self):
        return (set(self.pile1) | set(self.pile2)) == set(cards)

    def utility(self):
        """
        Utility based on the difference
        of piles from perfect score
        """
        # perfect score 360 + (10 * 36)

        pile1_raw_score = abs(sum(self.pile1) - 36)
        pile2_raw_score = abs(np.prod(self.pile2) - 360)
        d = pile1_raw_score + pile2_raw_score

        score = 720 * np.exp(-d)

        return score

    def is_goal(self):
        """
        check if goal state
        """

        if not self.is_valid():
            return False
        return sum(self.pile1) == 36 and np.prod(self.pile2) == 360

    @staticmethod
    def reproduce(father, mother):
        """
        Random reproduction
        """
        c = random.randint(0, 4)
        pile1 = father.pile1[:c] + mother.pile1[c:]
        pile2 = list(set(cards) - set(pile1))

        return Individual(pile1, pile2)

    def mutate(self):
        """
        mutate a random digit on the first pile
        """

        for i in range(5):

            # (40% chance of mutation)
            if np.random.choice([True, False], 1, [40, 60])[0]:
                # pick a digit from pile two and swap it with a digit on pile one
                p2 = random.randint(0, 4)

                self.pile1[i], self.pile1[p2] = self.pile1[p2], self.pile1[i]

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
        print('')

    def rep(self):
        _rep = ""

        for card in self.pile1:
            _rep += str(card)

        return _rep

    def __eq__(self, other):
        return other.rep() == self.rep()


def genetic_solver():
    size_of_initial_population = 100
    population = [Individual.random_individual() for i in range(size_of_initial_population)]
    total_children = 0

    report_data_x = []  # set of points to show on graph
    report_data_y = []  # set of points to show on graph

    while True:
        total_children += 1
        report_data_x.append(total_children)

        population_weights = [indv.utility() for indv in population]

        report_data_y.append(sum(population_weights) / len(population_weights))

        new_population = copy.deepcopy(population)

        for individual in population:
            if individual.is_goal():
                return individual, total_children, report_data_x, report_data_y

            # select parents
            father = np.random.choice(population, 1, population_weights)[0]
            mother = np.random.choice(population, 1, population_weights)[0]

            child1 = Individual.reproduce(father, mother)
            child2 = Individual.reproduce(mother, father)

            child1.mutate()
            child2.mutate()

            if child1.is_valid():
                new_population.append(child1)

            if child2.is_valid():
                new_population.append(child2)

        population = copy.deepcopy(new_population)


def test():
    number_of_tests = 10
    total_population_size = 0

    print("Running system test on %d test cases ..." % number_of_tests)

    for i in range(1, number_of_tests + 1):
        print('{0}/{1}'.format(i, number_of_tests), end='\r')
        solution, t, x, y = genetic_solver()
        total_population_size += t

    print("Average generation at the solution: %.2f" % (total_population_size / number_of_tests))


solution, t, x, y = genetic_solver()
print("Solution: ")
solution.print_me()
plt.plot(x, y, 'o', color="black")
plt.show()
test()
