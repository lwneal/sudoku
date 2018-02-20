import numpy as np
from functools import reduce

class Sudoku:
    def __init__(self, state=None):
        if state is None:
            # Height, Width, Number of Digits
            self.state = np.ones((9,9,9), dtype=bool)
        else:
            self.state = state

    def __repr__(self):
        is_known = self.state.sum(axis=2) == 1
        values = self.state.argmax(axis=2) + 1
        return str(values * is_known)

    def is_solved(self):
        # The state is solved when only a single value remains for each cell
        return np.all(self.state.sum(axis=2) == 1)

    def is_impossible(self):
        # If for any cell no value is possible, the puzzle cannot be solved
        return np.any(self.state.sum(axis=2) == 0)

    def inference(self, heuristic_level=5):
        heuristics = [
            self.heuristic_naked_singles,
            self.heuristic_hidden_singles,
            self.heuristic_naked_pairs,
            self.heuristic_hidden_pairs,
            self.heuristic_naked_triples,
            self.heuristic_hidden_triples,
        ][:heuristic_level]
        while any(h() for h in heuristics):
            # If any heuristic changes something, go back and re-run all the heuristics
            pass
        # Inference is done when every heuristic returns False

    def heuristic_naked_singles(self):
        is_known = self.state.sum(axis=2) == 1
        argmaxes = self.state.argmax(axis=2)
        old_state = self.state.copy()
        for y, x in np.ndindex(9, 9):
            if is_known[y, x]:
                assign_idx(self.state, y, x, argmaxes[y,x])
        # Return a nonzero value if this heuristic changed anything
        return np.any(self.state != old_state)

    def heuristic_hidden_singles(self):
        old_state = self.state.copy()
        for idx in range(9):
            for row in range(9):
                if self.state[row, :, idx].sum() == 1:
                    x = self.state[row, :, idx].argmax()
                    assign_idx(self.state, row, x, idx)
            for col in range(9):
                if self.state[:, col, idx].sum() == 1:
                    y = self.state[:, col, idx].argmax()
                    assign_idx(self.state, y, col, idx)
            for bx, by in np.ndindex(3, 3):
                box = self.state[by*3:3+by*3, bx*3:3+bx*3, idx]
                if box.sum() == 1:
                    y = 3*by + box.argmax(axis=0).max()
                    x = 3*bx + box.argmax(axis=1).max()
                    assign_idx(self.state, y, x, idx)
        # Return a nonzero value if this heuristic changed anything
        return np.any(self.state != old_state)

    def heuristic_naked_pairs(self):
        old_state = self.state.copy()
        # Each "idx" is a number (ie. a possible value from 1 to 9)
        for number_pair in pairs():
            # Each row is a y-coordinate. Row 0 is at the top of the 9x9 grid
            for row in range(9):
                naked_pair(self.state[row, :], number_pair)
            # Each column is an x-coordinate. Col 0 is on the left
            for col in range(9):
                naked_pair(self.state[:, col], number_pair)
            # There are 9 boxes, each is 3x3 and contains 9 squares
            for bx, by in np.ndindex(3, 3):
                box = self.state[by*3:by*3 + 3, bx*3:bx*3 + 3].reshape((9,9))
                result = naked_pair(box, number_pair)
                self.state[by*3:by*3 + 3, bx*3:bx*3 + 3] = result.reshape((3,3,9))
        return np.any(self.state != old_state)

    def heuristic_hidden_pairs(self):
        old_state = self.state.copy()
        for number_pair in pairs():
            for row in range(9):
                hidden_pair(self.state[row, :], number_pair)
            for col in range(9):
                hidden_pair(self.state[:, col], number_pair)
            for bx, by in np.ndindex(3, 3):
                box = self.state[by*3:by*3 + 3, bx*3:bx*3 + 3].reshape((9,9))
                result = hidden_pair(box, number_pair)
                self.state[by*3:by*3 + 3, bx*3:bx*3 + 3] = result.reshape((3,3,9))
        return np.any(self.state != old_state)

    def heuristic_naked_triples(self):
        old_state = self.state.copy()
        for cell_triple in triples():
            for row in range(9):
                naked_triple(self.state[row, :], cell_triple)
            for col in range(9):
                naked_triple(self.state[:, col], cell_triple)
            for bx, by in np.ndindex(3, 3):
                box = self.state[by*3:by*3 + 3, bx*3:bx*3 + 3].reshape((9,9))
                result = naked_triple(box, cell_triple)
                self.state[by*3:by*3 + 3, bx*3:bx*3 + 3] = result.reshape((3,3,9))
        return np.any(self.state != old_state)

    def heuristic_hidden_triples(self):
        old_state = self.state.copy()
        for cell_triple in triples():
            for row in range(9):
                hidden_triple(self.state[row, :], cell_triple)
            for col in range(9):
                hidden_triple(self.state[:, col], cell_triple)
            for bx, by in np.ndindex(3, 3):
                box = self.state[by*3:by*3 + 3, bx*3:bx*3 + 3].reshape((9,9))
                result = hidden_triple(box, cell_triple)
                self.state[by*3:by*3 + 3, bx*3:bx*3 + 3] = result.reshape((3,3,9))
        return np.any(self.state != old_state)

    def get_possible_actions(self, heuristic=False):
        assignments = []
        for y, x in np.ndindex(9,9):
            if self.state[y, x].sum() > 1:
                for idx in range(9):
                    if self.state[y, x, idx]:
                        value = idx + 1
                        assignments.append((y, x, value))
        def mrv(assignment):
            y, x, _ = assignment
            return self.state[y, x].sum()
        if heuristic:
            assignments.sort(key=mrv)
        return assignments
    
    def take_action(self, y, x, value):
        idx = value - 1
        assert 1 <= value <= 9
        assert self.state[y, x, idx]
        new_state = self.state.copy()
        assign_idx(new_state, y, x, idx)
        return Sudoku(new_state)



# Assigns a value and enforces the basic rules of Sudoku:
# ie. the alldiff constraints for rows, columns, and boxes
def assign_idx(state, y, x, idx):
    # Enforce consistency of rows/columns
    state[y,:,idx] = 0
    state[:,x,idx] = 0
    # Enforce consistency of boxes
    y0, x0 = (y // 3) * 3, (x // 3) * 3
    state[y0:y0 + 3, x0:x0 + 3, idx] = 0
    # Remove alternatives to this value
    state[y,x,:] = 0
    # Set the selected value
    state[y, x, idx] = 1
    return state


# Count all the distinct pairs of elements one through nine
def pairs():
    for i in range(9):
        for j in range(i + 1, 9):
            yield np.array([i, j])


# Count all the distinct triples of elements one through nine
def triples():
    for i in range(9):
        for j in range(i+1, 9):
            for k in range(j+1, 9):
                yield np.array([i, j, k])


# Given a group of 9 cells (row, column, or box) and two indices, is there a naked pair?
def naked_pair(group, pair):
    # For each cell
    for i in range(9):
        # If this cell can only be the given pair
        if group[i][pair].all() and group[i].sum() == 2:
            for j in range(i + 1, 9):
                # And if another cell can only be the given pair
                if all(group[j] == group[i]):
                    # Other cells CANNOT contain the given pair of numbers
                    group[:, pair] = False
                    group[i, pair] = True
                    group[j, pair] = True
    return group


# Given three cells, do they form a naked triple?
def naked_triple(group, cell_triple):
    # Does each cell have two possible numbers?
    if all(group[cell_triple].sum(1) == 2):
        # If you combine them, are there three numbers?
        if group[cell_triple].any(0).sum() == 3:
            # This is a naked triple
            values = [i for i, x in enumerate(group[cell_triple].any(0)) if x]
            for i in range(9):
                if i not in cell_triple:
                    group[i, values] = False
    return group


# Given a group of 9 cells, does the given pair of numbers form a hidden pair?
def hidden_pair(group, number_pair):
    # Does each number occur only twice?
    if all(s == 2 for s in group[:, number_pair].sum(0)):
        # Does each number occur twice in the same place?
        for cell_pair in pairs():
            if all(group[cell_pair, number].all() for number in number_pair):
                # Other numbers CANNOT occur in this pair of cells
                group[cell_pair, :] = False
                for i in cell_pair:
                    for j in number_pair:
                        group[i, j] = True
    return group


# Given three cells, do they form a hidden triple?
def hidden_triple(group, number_triple):
    # Does each number appear only three times?
    if all(s == 3 for s in group[:, number_triple].sum(0)):
        # Do they appear in the same three places?
        for cell_triple in triples():
            if all(group[cell_triple, number].all() for number in number_triple):
                # Hidden triple: other numbers cannot occur in these cells
                group[cell_triple, :] = False
                for i in cell_triple:
                    for j in number_triple:
                        group[i, j] = True
    return group
    

# Loads example problems of the format at:
# http://web.engr.oregonstate.edu/~tadepall/cs531/18/sudoku-problems.txt
def from_file(filename):
    state = load_txt(open(filename).read())
    return Sudoku(state)


def load_txt(text):
    state = np.ones((9,9,9), dtype=bool)
    for i, line in enumerate(lines(text)):
        for j, val in enumerate(line_to_ints(line)):
            if val > 0:
                assign_idx(state, i, j, val-1)
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
