# CMPT 317: Script for colored tile problem

# Copyright (c) 2022 Jeff Long
# Department of Computer Science, University of Saskatchewan

# This script solves a series of Colored Tile problems using
# IDS and displays the sequence of actions needed to 
# solve each problem
#


import UninformedSearch as BlindSearch
import coloredTiles as P

import sys as sys
import time as time

# process the command line arguments
#print(sys.argv)

if len(sys.argv) < 2:
    print('usage: python', sys.argv[0], 'problem_file time_limit')
    sys.exit()


timelimit = int(sys.argv[2])

file = open(sys.argv[1], 'r')

# read the examples first
examples = []
file = open(sys.argv[1], 'r')
line = file.readline()

while line:
    #read the puzzle dimension
    dims = int(line)
    puzzle = []
    for i in range(dims):
        line = file.readline().rstrip()
        puzzle.append(line)
    examples.append(puzzle)
    line = file.readline()

file.close()

# search using IDS and graph search
search_type = "graph"
problem_index = 1

for ex in examples:
    problem = P.Problem(len(ex), len(ex[0]), ex)
    s = problem.create_initial_state()
    searcher = BlindSearch.Search(problem, timelimit=timelimit)
    answer = searcher.IDS(s, search_type)
    if answer.success:
        print(answer.result.depth, "actions needed to solve problem",problem_index)
        s.display()
        # NOTE: Your state class needs to store the action that created it using a class variable called "action" in order to use this!
        answer.result.display_steps()
    else:
        print("Could not solve problem", problem_index)
    problem_index += 1
    print("----------------")



