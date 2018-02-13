"""
Solving Sudoku using Backtracking Search with Constraint Propagation
"""
import sys
import sudoku
import numpy as np


# The search begins by storing all possible values for each of the empty spots.
# Then it does constraint propagation through domain-specific inference rules.
# When the constraint propagation converges, then:
#   if no candidates left for some cell, then backtrack from the current state.
#   else pick a cell, and assign it a consistent value
def backtrack_search(prob):
    prob.inference()
    if prob.is_impossible():
        return None
    if prob.is_solved():
        return prob
    for y, x, val in prob.get_possible_actions():
        result = backtrack_search(prob.take_action(y, x, val))
        if result:
            return result
    assert False


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python {} puzzle.txt".format(sys.argv[0]))
        print("  For example puzzle.txt files see problems/")
        exit()
    su = sudoku.from_file(sys.argv[1])
    print("Original Problem:")
    print(su)
    solution = backtrack_search(su)
    print("Solution:")
    print(solution)
