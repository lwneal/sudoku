"""
Solving Sudoku using Backtracking Search with Constraint Propagation
"""
import sys
import time
import sudoku

backtrack_count = 0
MAX_BACKTRACK = 10

def backtrack_search(prob, heuristic_level=5, use_mrv=False):
    global backtrack_count
    prob.inference()
    if prob.is_impossible():
        backtrack_count += 1
        if backtrack_count > MAX_BACKTRACK:
            raise Exception("Too many backtracks")
        return None
    if prob.is_solved():
        return prob
    for y, x, val in prob.get_possible_actions(use_mrv):
        result = backtrack_search(prob.take_action(y, x, val))
        if result:
            return result
    backtrack_count += 1
    if backtrack_count > MAX_BACKTRACK:
        raise Exception("Too many backtracks")
    return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python {} puzzle.txt".format(sys.argv[0]))
        print("  For example puzzle.txt files see problems/")
        exit()
    filename = sys.argv[1]
    su = sudoku.from_file(filename)
    print("Original Problem:")
    print(su)
    start = time.time()
    try:
        solution = backtrack_search(su)
    except:
        solution = None
    duration = time.time() - start
    if solution:
        print("Solved {} with {} backtracks in {:.2f} sec:".format(filename, backtrack_count, duration))
        print(solution)
    else:
        print("Failed {} after hitting limit of {} backtracks".format(filename, backtrack_count))
