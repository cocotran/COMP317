These data files contain Colored Tile problems

a_tiles_easy.txt
b_tiles_medium.txt
c_tiles_hard.txt
d_tiles_nightmare.txt
e_tiles_impossible.txt

The file names are indicative of the average difficulty of problems in the files themselves.  Here, the measure of difficulty is the expected depth of the optimal solution in combination with the grid size, but as the problems are randomly generated (by randomly choosing tiles to touch from a solution state), some problem instances may be less difficult than the average for the data set.

Files will contain multiple problem instances.

A problem instance consists of an integer, N, by itself on a line, indicating the size of the tile grid for that problem.  N lines will follow, each consisting of a string of N characters, where each character is either G or R.  Example:

3
RGR
GGG
RRR
