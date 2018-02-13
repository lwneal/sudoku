import numpy as np


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
        # The state is solved when only a single value remains for each square
        return np.all(self.state.sum(axis=2) == 1)

    def is_impossible(self):
        # If for any square no value is possible, the puzzle cannot be solved
        return np.any(self.state.sum(axis=2) == 0)

    def inference(self):
        heuristics = [getattr(self, h) for h in dir(self) if h.startswith('heuristic')]
        while any(h() for h in heuristics):
            pass
        pass

    def heuristic_naked_singles(self):
        is_known = self.state.sum(axis=2) == 1
        argmaxes = self.state.argmax(axis=2)
        count = 0
        old_state = self.state.copy()
        for y, x in np.ndindex(9, 9):
            if is_known[y, x]:
                assign_idx(self.state, y, x, argmaxes[y,x])
        # Return a nonzero value if this heuristic changed anything
        return np.any(self.state != old_state)

    def heuristic_hidden_singles(self):
        # TODO
        pass

    def heuristic_naked_pairs(self):
        # TODO
        pass

    def heuristic_hidden_pairs(self):
        # TODO
        pass

    def heuristic_naked_triples(self):
        # TODO
        pass

    def heuristic_hidden_triples(self):
        # TODO
        pass

    def get_possible_actions(self, heuristic=True):
        assignments = []
        for y, x in np.ndindex(9,9):
            if self.state[y, x].sum() > 1:
                for idx in range(9):
                    if self.state[y, x, idx]:
                        value = idx + 1
                        assignments.append( (y, x, value) )
        def mcv(assignment):
            y, x, _ = assignment
            return self.state[y, x].sum()
        if heuristic:
            assignments.sort(key=mcv)
        print("{} assignments left".format(len(assignments)))
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
