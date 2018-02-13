"""
Solving Sudoku with Backtracking Search with Constraint Propagation

"""
import sys
import numpy as np

# Height, Width, Number of Digits
BOARD_SIZE = (9, 9, 9)

class Sudoku:
    def __init__(self, state=None):
        if state is None:
            self.state = np.ones((9,9,9), dtype=bool)
        else:
            self.state = state

    def __repr__(self):
        argmax = self.state.argmax(axis=2)
        argmax[self.state.max(axis=2) > 0] += 1
        return str(argmax)

    def is_solved(self):
        # The state is solved when only a single value remains for each square
        return np.all(self.state.sum(axis=2) == 1)

    def is_impossible(self):
        # If for any square no value is possible, the puzzle cannot be solved
        return np.any(self.state.sum(axis=2) == 0)

    def inference(self):
        # TODO: apply constraints to eliminate inconsistent values
        #Naked Singles
        #Hidden Singles.
        #Naked Pairs.
        #Hidden Pairs.
        #Naked Triples.
        #Hidden Triples.
        pass

    def consistent_assignments(self):
        for y in range(9):
            for x in range(9):
                if self.state[y, x].sum() > 1:
                    for val in range(1, 9):
                        # TODO: Check if y, x, val is consistent
                        if self.state[y, x, val - 1]:
                            yield y, x, val

    def assign_value(self, y, x, value):
        assert 1 <= value <= 9
        new_state = self.state.copy()
        print("Assigning pos {} {} value {}".format(y, x, value))
        new_state[y, x, :] = 0
        new_state[y, x, value - 1] = 1
        print(new_state[y,x])
        return Sudoku(new_state)


"""
Input format: Digits 1-9 for known squares, 0 for unused squares
    All non-digit 
Example input text:
000 006 009
090 300 108 
...
700 100 000 
"""
def sudoku_from_file(filename):
    state = load_txt(open(filename).read())
    return Sudoku(state)

def load_txt(text):
    state = np.ones((9,9,9), dtype=bool)
    for i, line in enumerate(lines(text)):
        for j, val in enumerate(line_to_ints(line)):
            if val > 0:
                state[i, j, :] = 0
                state[i, j, val - 1] = 1
    return state

def isdecimal(c):
    return '0' <= c <= '9'

def lines(text):
    for line in text.splitlines():
        if sum(isdecimal(c) for c in line) >= 9:
            yield line

def line_to_ints(line):
    for char in line:
        if isdecimal(char):
            yield int(char)

# The search begins by storing all possible values for each of the empty spots.
# Then it does constraint propagation through domain-specific inference rules.
# When the constraint propagation converges, then:
#- if no candidates left for some cell, then backtrack from the current state.
#- else pick a cell, and assign it a consistent value

def backtrack(su):
    su.inference()
    if su.is_solved():
        return su
    if su.is_impossible():
        print("Impossible")
        return None
    for y, x, val in su.consistent_assignments():
        print("Assigning {} {} value {}".format(y, x, val))
        result = backtrack(su.assign_value(y, x, val))
        if result:
            print("Returning correct result:\n{}".format(su))
            exit()
            return result

su = sudoku_from_file(sys.argv[1])
solution = backtrack(su)
print("Solution:")
print(solution)
