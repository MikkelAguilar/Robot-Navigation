# Robot-Navigation
A robot navigation project used to attain a High Distinction on the unit, 'Introduction to AI'. Makes use of custom written tree search algorithms to output a valid path for a robot to traverse a NxN grid.

How to use:
 - Navigate to the folder with 'main.py'
 - Change and modify the text file 'data.txt' to change the size of grid, position of the robot, walls nodes, and goal nodes
 - The first line represents the grid size [width, length], the second represents the robots starting node (x, y), the third represents the goal node (x, y) and all subsequent lines are the wall nodes and their respective width and height starting from the top right (x, y, width, length)
 - From the terminal type in, 'main.py data.txt BFS' (BFS can be replaced with other search methods - GBFS, AS, CUS1, CUS2)