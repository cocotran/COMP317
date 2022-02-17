#! /usr/bin/bash

python solver.py ../Data/a_tiles_easy.txt  > a_easy.out
python solver.py ../Data/b_tiles_medium.txt  > b_medium.out
python solver.py ../Data/c_tiles_hard.txt  > c_hard.out
python solver.py ../Data/d_tiles_nightmare.txt  > d_nightmare.out
python solver.py ../Data/e_tiles_impossible.txt  > e_impossible.out

