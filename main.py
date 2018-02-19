"""
Solving Sudoku using Backtracking Search with Constraint Propagation
"""
import sys
import sudoku

backtrack_count = 0
MAX_BACKTRACK = 100

def backtrack_search(prob, count=0):
    global backtrack_count
    prob.inference()
    if prob.is_impossible():
        backtrack_count += 1
        if backtrack_count > MAX_BACKTRACK:
            raise Exception("Too many backtracks")
        return None
    if prob.is_solved():
        return prob
    for y, x, val in prob.get_possible_actions():
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
    su = sudoku.from_file(sys.argv[1])
    print("Original Problem:")
    print(su)
    solution = backtrack_search(su)
    if solution:
        print("Solution (required {} backtracks):".format(backtrack_count))
        print(solution)
    else:
        print("FAILURE: NO SOLUTION")
        exit(1)
