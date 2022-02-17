import sys as sys
import random as rand
import coloredTiles as P

def state_string(s):
    answer = ""
    puzzle = s.puzzle
    answer += str(len(puzzle)) + "\n"
    for row in puzzle:
        for val in row:
            if val:
                answer += "G"
            else:
                answer += "R"
        answer += "\n"
        
    return answer
        
if len(sys.argv) < 4:
    print('usage: python', sys.argv[0], 'num_samples gridsize solution_depth')
    sys.exit()
        
num_samples = int(sys.argv[1])
dims = int(sys.argv[2])
depth = int(sys.argv[3])

start = []
for r in range(dims):
    row = []
    for c in range(dims):
        row.append(True)
    start.append(row)

for samp in range(num_samples):        
    s = P.State(start)
    for d in range(depth):
        x = rand.randint(0, dims-1)
        y = rand.randint(0, dims-1)
        s.touch(x, y)
    print(state_string(s), end="")