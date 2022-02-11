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
import coloredTiles as P
import roots as roots
import Statistics

import gc as gc
import sys as sys
import time as time

# process the command line arguments
print(sys.argv)

if len(sys.argv) < 3:
    print('usage: python', sys.argv[0], 'examplefile timelimit depthlimit')
    sys.exit()

file = open(sys.argv[1], 'r')
timelimit = int(sys.argv[2])
depth_limit = int(sys.argv[3])

strategies = ['BFS', 'DFS', 'DLS', 'IDS']
search_types = ["tree", "graph"]


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

predicted_time = len(search_types)*len(strategies)*timelimit*len(examples)
print('Estimated maximum time to solve', sys.argv[0], 'using strategies:', strategies, 'is', predicted_time, 'seconds')
global_start = time.time()

# try all the solvers
for search_type in search_types:
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

            if solver == 'BFS':
                problem = P.Problem(len(ex), len(ex[0]), ex)
                s = problem.create_initial_state()
                searcher = BlindSearch.Search(problem, timelimit=timelimit)
                answer = searcher.BreadthFirstSearch(s, search_type)

            elif solver == 'DFS':
                problem = P.Problem(len(ex), len(ex[0]), ex)
                s = problem.create_initial_state()
                searcher = BlindSearch.Search(problem, timelimit=timelimit)
                answer = searcher.DepthFirstSearch(s, search_type)

            elif solver == 'DLS':
                problem = P.Problem(len(ex), len(ex[0]), ex)
                s = problem.create_initial_state()
                searcher = BlindSearch.Search(problem, timelimit=timelimit)
                answer = searcher.DepthLimitedSearch(s, depth_limit, search_type)

            elif solver == 'IDS':
                problem = P.Problem(len(ex), len(ex[0]), ex)
                s = problem.create_initial_state()
                searcher = BlindSearch.Search(problem, timelimit=timelimit)
                answer = searcher.IDS(s, search_type)

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
    #             print(ex, answer.result.depth, answer.success, checked,
    #                   answer.time, answer.nodes, answer.space)

                ebf_stat.add(roots.eff_br_fact(answer.nodes, answer.result.depth))
                depth_stat.add(answer.result.depth)
            else:
                count_unsolved += 1
    #             print(ex, None, answer.success, None, answer.time, answer.nodes, answer.space, '*****')

            time_stat.add(answer.time)
            nodes_stat.add(answer.nodes/answer.time)
            space_stat.add(answer.space)

        # print a summary of all the examples
        print()
        print('Summary for',solver,'using',search_type,'search on data set',sys.argv[0])
        print("Attempted:", len(examples))
        print("Solved:", len(examples) - count_unsolved)
        print("Average depth:", depth_stat.mean())
        print("Average time:", time_stat.mean())
        print("Average space:", space_stat.mean())
        print("Average effective branching factor:", ebf_stat.mean())
        print("Average nodes per second:", nodes_stat.mean())
        print("Maximum time:", time_stat.max())
        print("Maximum depth:", depth_stat.max())
        print("Time cutoff:", timelimit)
        print("Total time:", time_stat.mean()*time_stat.count())
        print("\n")
        
global_finish = time.time()
print('Took', global_finish - global_start, 'seconds (predicted', predicted_time, 'seconds)')