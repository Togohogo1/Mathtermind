from itertools import combinations_with_replacement as cwr

from classes.classic_solver import ClassicSolver


class RepeatSolver(ClassicSolver):
    def __init__(self, rounds, matches, verified):
        super().__init__(rounds, matches, verified)
        self.combos = list(cwr(range(1, 16), 3))
