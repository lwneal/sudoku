"""
Solving Sudoku using Backtracking Search with Constraint Propagation
"""
import sys
import sudoku

backtrack_count = 0

def backtrack_search(prob, count=0):
    global backtrack_count
    prob.inference()
    if prob.is_impossible():
        print("Backtracking")
        backtrack_count += 1
        return None
    if prob.is_solved():
        return prob
    for y, x, val in prob.get_possible_actions():
        result = backtrack_search(prob.take_action(y, x, val))
        if result:
            return result
    print("Backtracking")
    backtrack_count += 1
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
    print("Solution (required {} backtracks):".format(backtrack_count))
    print(solution)
