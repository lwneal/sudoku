#!/bin/bash
set -e

echo "Running Sudoku solver"


for heuristic_level in 0 1 2 3 4 5; do 
    OUTPUT_FILENAME="results_heuristic_level_$heuristic_level.txt"
    for difficulty in easy medium hard evil; do
        echo "Attempting to solve all problems difficulty $difficulty heuristic level $heuristic_level"
        for filename in `find problems/ | grep $difficulty`; do
            echo "Solving $filename with heuristic level $heuristic_level"
            python main.py $filename $heuristic_level >> $OUTPUT_FILENAME
        done
    done
done
