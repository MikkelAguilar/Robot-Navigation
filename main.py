from re import X
import sys
from robot import Robot

valid_search_methods = ['DFS', 'BFS', 'GBFS', 'AS', 'CUS1', 'CUS2', 'ALL']
separator = ['-'] * 30

if __name__ == '__main__':
    #Check if arguments given are in the correct format
    if len(sys.argv) != 3 or sys.argv[2].upper() not in valid_search_methods:
        print("Incorrect Format")
        sys.exit()
    
    file = sys.argv[1] #Assign file to the second argument
    robot = Robot()

    #Try to read from the file, but if file is not found, end the program
    try:
        robot.read_from_file(file)
    except FileNotFoundError:
        print('File name does not exist')
        sys.exit()
    
    if sys.argv[2].upper() == 'ALL': #Find the shortest path to all goals
        x = robot.shortest_path_to_all_goals(robot.starting_location, robot.goals)
        if x != None:
            print(', '.join(x))
        else:
            print('Cannot find path')
    else: #Loops through each goal and prints the path and the number of visited nodes
        for i in range(len(robot.goals)):
            print(f"Goal {str(i + 1)} - " + str(robot.goals[i]))
            print("".join(separator))
            robot.search_stats(sys.argv[2], robot.goals[i])