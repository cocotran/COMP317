# CMPT 317: CSPs on the Colored Tile problem

# Copyright (c) 2022 Jeff Long
# Department of Computer Science, University of Saskatchewan

# This script reads Colored Tile problems from file, and for each one,
# outputs a CSP formalization (variables, domains, constraints)
#

import sys as sys

if len(sys.argv) < 1:
    print('usage: python', sys.argv[0], 'problem_file')
    sys.exit()

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

num = 1
for p in examples:
    print("------")
    print("CSP for problem", num)
    #TODO: analyze p to produce appropriate variables, domains and constraitns
    # print out that info here
    print("...")
    print("------")
    num += 1