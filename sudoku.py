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
        # The state is solved when only a single value remains for each square
        return np.all(self.state.sum(axis=2) == 1)

    def is_impossible(self):
        # If for any square no value is possible, the puzzle cannot be solved
        return np.any(self.state.sum(axis=2) == 0)

    def inference(self):
        # If any heuristic changes something, go back and re-run all the heuristics
        while True:
            if self.heuristic_naked_singles():
                continue
            if self.heuristic_hidden_singles():
                continue
            
            if self.heuristic_naked_pairs():
                continue
            
            if self.heuristic_hidden_pairs():
                continue
            
            if self.heuristic_naked_triples():
                continue
            if self.heuristic_hidden_triples():
                continue
            
            
            # Every heuristic is finished running: inference is done now
            break

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
        for idx in range(9):
            for partner_idx in range(idx + 1, 9):
                pair = np.array([idx, partner_idx])
                # Each row is a y-coordinate. Row 0 is at the top of the 9x9 grid
                for row in range(9):
                    naked_pair(self.state[row, :], pair)
                # Each column is an x-coordinate. Col 0 is on the left
                for col in range(9):
                    naked_pair(self.state[:, col], pair)
                # There are 9 boxes, each is 3x3 and contains 9 squares
                for bx, by in np.ndindex(3, 3):
                    box = self.state[by*3:by*3 + 3, bx*3:bx*3 + 3].reshape((9,9))
                    naked_pair(box, pair)
        return np.any(self.state != old_state)

    def heuristic_hidden_pairs(self):
        old_state = self.state.copy()
        for idx in range(9):
            for row in range(9):
                #get current box 
                cur_space = self.state[row,idx]
                cur_space_indices = [i for i, x in enumerate(cur_space) if x == True] 
                #search all other spaces
                for partner in range(9):
                    if partner == idx: continue
                    partner_space = self.state[row,partner]
                    partner_space_indices = [i for i, x in enumerate(partner_space) if x == True] 

                    #find the common numbers between two arbitrary spaces
                    intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                    if len(intersect) == 2:
                        
                        break_partner = False
                        for other in range(9):
                            if other == idx: continue
                            if other == partner: continue
                        
                            other_space = self.state[row,other]
                            other_space_indices = [i for i, x in enumerate(other_space) if x == True] 
                            #see if the common pair is unique
                            other_intersect = np.intersect1d(intersect,other_space_indices)
                            if (len(other_intersect) > 0):
                                #if it is, quit your partner
                                break_partner = True
                                break

                        #we java now
                        if break_partner: break

                        #actually apply the inference
                        self.state[row,idx] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
                        self.state[row,partner] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
            for col in range(9):
                #get current box 
                cur_space = self.state[idx, col]
                cur_space_indices = [i for i, x in enumerate(cur_space) if x == True] 
                #search all other spaces
                for partner in range(9):
                    if partner == idx: continue
                    partner_space = self.state[partner, col]
                    partner_space_indices = [i for i, x in enumerate(partner_space) if x == True] 

                    #find the common numbers between two arbitrary spaces
                    intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                    if len(intersect) == 2:
                        
                        break_partner = False
                        for other in range(9):
                            if other == idx: continue
                            if other == partner: continue
                        
                            other_space = self.state[col,idx] 
                            other_space_indices = [i for i, x in enumerate(other_space) if x == True] 
                            #see if the common pair is unique
                            other_intersect = np.intersect1d(intersect,other_space_indices)
                            if (len(other_intersect) > 0):
                                #if it is, quit your partner
                                break_partner = True
                                break

                        #we java now
                        if break_partner: break

                        #actually apply the inference
                        self.state[idx, col ] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
                        self.state[partner, col] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
        
        for ix, iy in np.ndindex(3, 3):
            cur_box = self.state[iy*3:3+iy*3, ix*3:3+ix*3].reshape((9,9))
            for idx in range(9):
                #get current box 
                cur_space = cur_box[idx]
                cur_space_indices = [i for i, x in enumerate(cur_space) if x == True] 
                #search all other spaces
                for partner in range(9):
                    if partner == idx: continue
                    partner_space = cur_box[partner]
                    partner_space_indices = [i for i, x in enumerate(partner_space) if x == True] 

                    #find the common numbers between two arbitrary spaces
                    intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                    if len(intersect) == 2:
                        
                        break_partner = False
                        for other in range(9):
                            if other == idx: continue
                            if other == partner: continue
                        
                            other_space = cur_box[other]
                            other_space_indices = [i for i, x in enumerate(other_space) if x == True] 
                            #see if the common pair is unique
                            other_intersect = np.intersect1d(intersect,other_space_indices)
                            if (len(other_intersect) > 0):
                                #if it is, quit your partner
                                break_partner = True
                                break

                        #we java now
                        if break_partner: break

                        #actually apply the inference
                        cur_box[idx] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
                        cur_box[partner] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
            self.state[iy*3:3+iy*3, ix*3:3+ix*3] = cur_box.reshape((3,3,9))
            
        return np.any(self.state != old_state)

    def heuristic_naked_triples(self):
        old_state = self.state.copy()
        for triple in range(9):
            for partner in range(9):
                for idx in range(9):
                    if triple == partner: continue
                    if idx == partner: continue
                    if idx == triple : continue

                    for row in range(9):
                       
                        cur_space     = self.state[row,idx]
                        partner_space = self.state[row,partner]
                        triple_space  = self.state[row,triple]

                        if cur_space.sum() == 2 and partner_space.sum() == 2 and triple_space.sum() == 2:
                            cur_space_indices     = [i for i, x in enumerate(cur_space) if x == True]
                            partner_space_indices = [i for i, x in enumerate(partner_space) if x == True]
                            triple_space_indices  = [i for i, x in enumerate(triple_space) if x == True]

                            cp_intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                            pt_intersect = np.intersect1d(partner_space_indices,triple_space_indices)
                            tc_intersect = np.intersect1d(triple_space_indices,cur_space_indices)

                            union = reduce(np.union1d, (cp_intersect, pt_intersect, tc_intersect))

                            if len(union) == 3:
                                # remove the union numbers from the rest
                                for rest in range(9):
                                    if rest == idx or rest ==partner or rest == triple: continue
                                    self.state[row,rest][union[0]] = False
                                    self.state[row,rest][union[1]] = False
                                    self.state[row,rest][union[2]] = False

                    for col in range(9):
                        cur_space     = self.state[idx,col]
                        partner_space = self.state[partner, col]
                        triple_space  = self.state[triple,  col]

                        if cur_space.sum() == 2 and partner_space.sum() == 2 and triple_space.sum() == 2:
                            cur_space_indices     = [i for i, x in enumerate(cur_space) if x == True]
                            partner_space_indices = [i for i, x in enumerate(partner_space) if x == True]
                            triple_space_indices  = [i for i, x in enumerate(triple_space) if x == True]

                            cp_intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                            pt_intersect = np.intersect1d(partner_space_indices,triple_space_indices)
                            tc_intersect = np.intersect1d(triple_space_indices,cur_space_indices)

                            union = reduce(np.union1d, (cp_intersect, pt_intersect, tc_intersect))

                            if len(union) == 3:
                                # remove the union numbers from the rest
                                for rest in range(9):
                                    if rest == idx or rest ==partner or rest == triple: continue
                                    self.state[rest ,col][union[0]] = False
                                    self.state[rest ,col][union[1]] = False
                                    self.state[rest ,col][union[2]] = False

            
                    for ix, iy in np.ndindex(3, 3):
                        cur_box = self.state[iy*3:3+iy*3, ix*3:3+ix*3].reshape((9,9))
                       
                        cur_space     = cur_box[idx]
                        partner_space = cur_box[partner]
                        triple_space  = cur_box[triple]

                        if cur_space.sum() == 2 and partner_space.sum() == 2 and triple_space.sum() == 2:
                            cur_space_indices     = [i for i, x in enumerate(cur_space) if x == True]
                            partner_space_indices = [i for i, x in enumerate(partner_space) if x == True]
                            triple_space_indices  = [i for i, x in enumerate(triple_space) if x == True]

                            cp_intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                            pt_intersect = np.intersect1d(partner_space_indices,triple_space_indices)
                            tc_intersect = np.intersect1d(triple_space_indices,cur_space_indices)

                            union = reduce(np.union1d, (cp_intersect, pt_intersect, tc_intersect))

                            if len(union) == 3:
                                # remove the union numbers from the rest
                                for rest in range(9):
                                    if rest == idx or rest ==partner or rest == triple: continue
                                    cur_box[rest][union[0]] = False
                                    cur_box[rest][union[1]] = False
                                    cur_box[rest][union[2]] = False
                        self.state[iy*3:3+iy*3, ix*3:3+ix*3] = cur_box.reshape((3,3,9))
        return np.any(self.state != old_state)

    #TODO: refactor this into "hidden n"
    def heuristic_hidden_triples(self):
        old_state = self.state.copy()
        for idx in range(9):
            for row in range(9):
                #get current box 
                cur_space = self.state[row,idx]
                cur_space_indices = [i for i, x in enumerate(cur_space) if x == True] 
                #search all other spaces
                for partner in range(9):
                    if partner == idx: continue
                    partner_space = self.state[row,partner]
                    partner_space_indices = [i for i, x in enumerate(partner_space) if x == True] 

                    #find the common numbers between two arbitrary spaces
                    intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                    if len(intersect) == 3:
                        
                        break_partner = False
                        for other in range(9):
                            if other == idx: continue
                            if other == partner: continue
                        
                            other_space = self.state[row,other]
                            other_space_indices = [i for i, x in enumerate(other_space) if x == True] 
                            #see if the common pair is unique
                            other_intersect = np.intersect1d(intersect,other_space_indices)
                            if (len(other_intersect) > 0):
                                #if it is, quit your partner
                                break_partner = True
                                break

                        #we java now
                        if break_partner: break

                        #actually apply the inference
                        self.state[row,idx] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
                        self.state[row,partner] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
            for col in range(9):
                #get current box 
                cur_space = self.state[idx, col]
                cur_space_indices = [i for i, x in enumerate(cur_space) if x == True] 
                #search all other spaces
                for partner in range(9):
                    if partner == idx: continue
                    partner_space = self.state[partner, col]
                    partner_space_indices = [i for i, x in enumerate(partner_space) if x == True] 

                    #find the common numbers between two arbitrary spaces
                    intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                    if len(intersect) == 3:
                        
                        break_partner = False
                        for other in range(9):
                            if other == idx: continue
                            if other == partner: continue
                        
                            other_space = self.state[col,idx] 
                            other_space_indices = [i for i, x in enumerate(other_space) if x == True] 
                            #see if the common pair is unique
                            other_intersect = np.intersect1d(intersect,other_space_indices)
                            if (len(other_intersect) > 0):
                                #if it is, quit your partner
                                break_partner = True
                                break

                        #we java now
                        if break_partner: break

                        #actually apply the inference
                        self.state[idx, col ] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
                        self.state[partner, col] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]

        for ix, iy in np.ndindex(3, 3):
            cur_box = self.state[iy*3:3+iy*3, ix*3:3+ix*3].reshape((9,9))
            for idx in range(9):
                #get current box 
                cur_space = cur_box[idx]
                cur_space_indices = [i for i, x in enumerate(cur_space) if x == True] 
                #search all other spaces
                for partner in range(9):
                    if partner == idx: continue
                    partner_space = cur_box[partner]
                    partner_space_indices = [i for i, x in enumerate(partner_space) if x == True] 

                    #find the common numbers between two arbitrary spaces
                    intersect = np.intersect1d(cur_space_indices,partner_space_indices)
                    if len(intersect) == 3:
                        
                        break_partner = False
                        for other in range(9):
                            if other == idx: continue
                            if other == partner: continue
                        
                            other_space = cur_box[other]
                            other_space_indices = [i for i, x in enumerate(other_space) if x == True] 
                            #see if the common pair is unique
                            other_intersect = np.intersect1d(intersect,other_space_indices)
                            if (len(other_intersect) > 0):
                                #if it is, quit your partner
                                break_partner = True
                                break

                        #we java now
                        if break_partner: break

                        #actually apply the inference
                        cur_box[idx] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
                        cur_box[partner] = [True if np.isin(i,list(intersect)) else False for i in range(9) ]
            self.state[iy*3:3+iy*3, ix*3:3+ix*3] = cur_box.reshape((3,3,9))

        return np.any(self.state != old_state)

    def get_possible_actions(self, heuristic=True):
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

# Given a group of 9 squares (row, column, or box) and two indices, is there a naked pair?
def naked_pair(group, pair):
    for i in range(9):
        if group[i][pair].all() and not group[i][~pair].any():
            for j in range(i + 1, 9):
                if all(group[j] == group[i]):
                    group[[i, j], ~pair] = False
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
