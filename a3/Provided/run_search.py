# CMPT 317: Solver script for solving Colored Tile problems

# Copyright (c) 2016-2022 Michael C Horsch, Jeffrey R Long
# Department of Computer Science, University of Saskatchewan

# This file is provided solely for the use of CMPT 317 students.  Students are permitted
# to use this file for their own studies, and to make copies for their own personal use.

# This file should not be posted on any public server, or made available to any party not
# enrolled in CMPT 317.

# This implementation is provided on an as-is basis, suitable for educational purposes only.
#


import UninformedSearch as BlindSearch
import InformedSearch as Search
import coloredTiles as P
import roots as roots
import Statistics

import gc as gc
import sys as sys
import time as time

# process the command line arguments
print(sys.argv)

if len(sys.argv) < 3:
    print('usage: python', sys.argv[0], 'examplefile timelimit')
    sys.exit()

file = open(sys.argv[1], 'r')
timelimit = int(sys.argv[2])



strategies = ['AStar0', 'AStarH1', 'AStarH2']

# read the examples first
examples = []
file = open(sys.argv[1], 'r')
line = file.readline()

while line:
    #read the puzzle dimension
    dims = int(line)
    # create a list of strings for the puzzle
    puzzle = []
    for i in range(dims):
        line = file.readline().rstrip()
        puzzle.append(line)
    examples.append(puzzle)
    line = file.readline()

predicted_time = len(strategies)*timelimit*len(examples)
print('Estimate for the time to solve', sys.argv[1], 'using strategies:', strategies, 'is', predicted_time, 'seconds')
global_start = time.time()

# try all the solvers
for solver in strategies:
    max_time = -1
    max_depth = -1
    count_unsolved = 0
    total_time = 0
    depth_stat = Statistics.Statistics()
    time_stat = Statistics.Statistics()
    ebf_stat = Statistics.Statistics()
    nodes_stat = Statistics.Statistics()
    space_stat = Statistics.Statistics()

#     print('Details for',solver,'on data set',sys.argv[1])
#     
#     print('index :', 'target', 'size', 'depth', 'success', 'checked', 'time', 'nodes', 'space')

    for ex in examples:
        gc.collect()  # clean up any allocated memory now, before we start timing stuff


        if solver == 'AStar0':
            problem = P.InformedProblem(len(ex), len(ex[0]), ex)
            s = problem.create_initial_state()
            searcher = Search.InformedSearch(problem, timelimit=timelimit)
            answer = searcher.AStarSearch(s)

        elif solver == 'AStarH1':
            problem = P.InformedProblemV1(len(ex), len(ex[0]), ex)
            s = problem.create_initial_state()
            searcher = Search.InformedSearch(problem, timelimit=timelimit)
            answer = searcher.AStarSearch(s)

        elif solver == 'AStarH2':
            problem = P.InformedProblemV2(len(ex), len(ex[0]), ex)
            s = problem.create_initial_state()
            searcher = Search.InformedSearch(problem, timelimit=timelimit)
            answer = searcher.AStarSearch(s)

        else:
            print('Unknown solver:', solver, '-- terminating!')
            sys.exit(1)

        # process the result of search
        if answer.success:
            # a weak check: if the specified goal state is equal to the returned goal state
            # could be stronger if the sequence of actions were checked
            checked = (answer.result.state.puzzle == problem.goal_state.puzzle)

            # print the actions
            # answer.result.display_steps()

            # display the details about this example
#             print(ex[0], ':', ex[1], ex[2], answer.result.depth, answer.success, checked,
#                   answer.time, answer.nodes, answer.space)

            ebf_stat.add(roots.eff_br_fact(answer.nodes, answer.result.depth))
            depth_stat.add(answer.result.depth)
        else:
            count_unsolved += 1
#             print(ex[0], ':', ex[1], ex[2], None, answer.success, None, answer.time, answer.nodes, answer.space, '*****')

        time_stat.add(answer.time)
        nodes_stat.add(answer.nodes/answer.time)
        space_stat.add(answer.space)

    # print a summary of all the examples
    print()
    print('Summary for',solver,'on data set',sys.argv[1])
    print("Attempted:", len(examples))
    print("Solved:", len(examples) - count_unsolved)
    print("Average depth:", depth_stat.mean())
    print("Average time:", time_stat.mean())
    print("Average space:", space_stat.mean())
    #print("Average effective branching factor:", ebf_stat.mean())
    #print("Average nodes per second:", nodes_stat.mean())
    #print("Maximum time:", time_stat.max())
    #print("Maximum depth:", depth_stat.max())
    #print("Time cutoff:", timelimit)
    #print("Total time:", time_stat.mean()*time_stat.count())
    print("\n")
global_finish = time.time()
print('Took', global_finish - global_start, 'seconds (predicted', predicted_time, 'seconds)')