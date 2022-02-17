# CMPT 317: Simple solver for testing purposes with local search


import math
import sys
import time
import coloredTiles as problem
import localsearch as search


# process the command line
if len(sys.argv) != 2:
    print('Usage: python3', sys.argv[0], '<filename>')
    sys.exit()


file = open(sys.argv[1], 'r')
line = file.readline()
puzzles = []
N = 0
while line:
    #read the puzzle dimension
    dims = int(line)
    N = dims
    puzzle = []
    for i in range(dims):
        line = file.readline().rstrip()
        puzzle.append(line)
    line = file.readline()
    p = problem.Problem(dims, dims, puzzle)
    puzzles.append(p)
    
steps = 1000

for p in puzzles:
    solution = search.random_search(p, steps)
    solution.display()
    print()
