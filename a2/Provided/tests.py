
import sys as sys
import coloredTiles as P

file = open(sys.argv[1], 'r')
line = file.readline()
puzzles = []
while line:
    #read the puzzle dimension
    print(line)
    dims = int(line)
    puzzle = []
    for i in range(dims):
        line = file.readline().rstrip()
        puzzle.append(line)
    line = file.readline()
    p = P.Problem(dims, dims, puzzle)
    print(p.init_state)
    print(p.goal_state)
    print(p.init_state.action)
    print("Goal?", p.is_goal(p.init_state))
    puzzles.append(p)
    
print(puzzles[0].result(puzzles[0].init_state, (1, 1)))
    