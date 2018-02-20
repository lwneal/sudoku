"""
Solving Sudoku using Backtracking Search with Constraint Propagation
"""
import sys
import time
import sudoku

backtrack_count = 0
MAX_BACKTRACK = 100

def backtrack_search(prob, heuristic_level=5, use_mrv=False):
    global backtrack_count
    prob.inference(heuristic_level)
    if prob.is_impossible():
        backtrack_count += 1
        if backtrack_count > MAX_BACKTRACK:
            raise Exception("Too many backtracks")
        return None
    if prob.is_solved():
        return prob
    for y, x, val in prob.get_possible_actions(use_mrv):
        result = backtrack_search(prob.take_action(y, x, val), heuristic_level, use_mrv)
        if result:
            return result
    backtrack_count += 1
    if backtrack_count > MAX_BACKTRACK:
        raise Exception("Too many backtracks")
    return None


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: sudoku.py puzzle.txt [heuristic_level] [use_mrv]")
        print("\tpuzzle.txt: Sudoku input text file")
        print("\theuristic_level: Integer 0 through 5, default 5")
        print("\tuse_mrv: True or False, default True")
        print("For example puzzle.txt files see problems/")
        exit()
    filename = sys.argv[1]
    heuristic_level = 5
    if len(sys.argv) > 2:
        heuristic_level = int(sys.argv[2])
    use_mrv = True
    if len(sys.argv) > 3:
        use_mrv = bool(sys.argv[3])
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
        print("Solved {} heuristic_level {} mrv {} with {} backtracks in {:.2f} sec:".format(
            filename, heuristic_level, use_mrv, backtrack_count, duration))
        print(solution)
    else:
        print("Failed {} after hitting limit of {} backtracks".format(filename, backtrack_count))
