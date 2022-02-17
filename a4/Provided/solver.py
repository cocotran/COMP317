# CMPT 317: More complete solver for collecting data on Local Search problems

# Copyright (c) 2016-2022 Michael C Horsch, Jeffrey R Long
# Department of Computer Science, University of Saskatchewan

import math
import sys
import time
import coloredTiles as problem
import localsearch as search
from Statistics import Statistics


# process the command line
if len(sys.argv) != 2:
    print('Usage: python3', sys.argv[0], '<filename>')
    sys.exit()

filename = sys.argv[1]
file = open(filename, 'r')

line = file.readline()
examples = []
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
    examples.append(p)
    


# because the local searches are randomized, use an average to report the results
repeats = 10

stepsrange = [100, 500, 1000, 2000]


err_stat_collection = {}
time_stat_collection = {}
# use all the strategies.  
strats = ['RG', 'RS', 'SHC', 'HC', 'RRHC1', 'RRHC2']
#strats = ["RRHC2"]
for strat in strats:

    for steps in stepsrange:
        print('Starting', strat, steps)
        
        err_stat_collection[strat,steps] = Statistics()
        time_stat_collection[strat,steps] = Statistics()
        for theProblem in examples:

            for i in range(repeats):
                if strat == 'RG':
                    start = time.perf_counter()
                    solution = search.random_guessing(theProblem, steps)
                    end = time.perf_counter()
                elif strat == 'RS':
                    start = time.perf_counter()
                    solution = search.random_search(theProblem, steps)
                    end = time.perf_counter()
                elif strat == 'HC':
                    start = time.perf_counter()
                    solution = search.hillclimbing(theProblem, steps)
                    end = time.perf_counter()
                elif strat == 'SHC':
                    start = time.perf_counter()
                    solution = search.stochastic_hillclimbing(theProblem, steps)
                    end = time.perf_counter()
                elif strat == 'RRHC1':
                    # short hill-climbing runs, but maybe a lot of them
                    start = time.perf_counter()
                    solution = search.random_restart(theProblem, steps // 20, 20)
                    end = time.perf_counter()
                elif strat == 'RRHC2':
                    # longer hill-climbing runs, but fewer of them
                    start = time.perf_counter()
                    solution = search.random_restart(theProblem, steps // 100, 100)
                    end = time.perf_counter()
                else:
                    # this should never happen, but you never know
                    print('Unknown strategy', strat)

                # collect the performance data for the run
                err_stat_collection[strat,steps].add(theProblem.objective_function(solution))
                time_stat_collection[strat,steps].add( end - start )
                
                # displaying the solution is a bit noisy, but useful in debugging
    #             print(' '.join(solution.program), theProblem.objective_function(solution))
    #         print('done (total time: {:.3}s)'.format(repeats*time_stat_collection[strat,steps].mean()))


def print_latex(strats, err_stat_collection, time_stat_collection, stepsrange):
    print()
    print('Averages table for', filename)
    for strat in strats:
        print('\\bf', strat, end=' ')
        for steps in stepsrange:
            # make the data look nice in text
            print(' & {:.1f} & {:.2e}'.format(err_stat_collection[strat,steps].mean(),   
                                              time_stat_collection[strat,steps].mean()), 
                                              end='')
        print(' \\\\')

        print('\\multicolumn{1}{r|}{(stdev)}', end=' ')
        for steps in stepsrange:
            # make the data look nice in text
            print(' & ({:.1e}) & ({:.1e}) '.format(math.sqrt(err_stat_collection[strat,steps].var()),   
                                              math.sqrt(time_stat_collection[strat,steps].var())), 
                                              end='')
        print(' \\\\')
        print('\\multicolumn{1}{r|}{(min)}', end=' ')
        for steps in stepsrange:
            # make the data look nice in text
             print(' & {} & '.format(err_stat_collection[strat,steps].min()),  
                                              end='')
        print(' \\\\\\hline')
        print()
        
def print_plain_text(strats, err_stat_collection, time_stat_collection, stepsrange):
    print()
    print('Averages table for', filename)
    for strat in strats:
        for steps in stepsrange:
            # make the data look nice in text
            print(strat, "Steps", steps, "Score {:.1f}".format(err_stat_collection[strat,steps].mean()), "Time {:.2e}".format(time_stat_collection[strat,steps].mean()))
            
#print_latex(strats, err_stat_collection, time_stat_collection, stepsrange)
print_plain_text(strats, err_stat_collection, time_stat_collection, stepsrange)
                                            
# eof
