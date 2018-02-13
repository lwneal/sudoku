#!/bin/bash

echo "Running Sudoku solver"

for level in easy medium hard evil; do
    echo "Attempting to solve all problems at level $level"
    for i in `find problems/ | grep $level`; do
        python main.py $i;
    done
    echo
done
