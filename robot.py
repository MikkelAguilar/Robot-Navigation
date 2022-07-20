from queue import Empty
import re
from nodes import Node

class Robot:
    def __init__(self): #Initialize all the variables which are initially empty until they are read from a file
        self.rows = None
        self.columns = None
        self.starting_location = None
        self.walls = []
        self.goals = []
        self.nodes = []
        self.current_position = None
        self.path_found = []
        self.real_path = []
        self.no_of_visited = None

    def read_from_file(self, filename): #Read all data from file, set variables to values from the file
        file = open(filename, 'r')
        lines = []
        length_of_file = len(file.readlines())
        number_of_walls = length_of_file - 3
        file.seek(0) #Set the starting point from the beginning of the file

        for i in range(length_of_file):
            lines.append(re.findall('[0-9]+', file.readline())) #Regular expression used to find the number values from the strings given in the text file

        #All variables are set to integers
        self.rows = int(lines[0][0])
        self.columns = int(lines[0][1])
        self.starting_location = (int(lines[1][0]), int(lines[1][1]))

        no_of_goals = len(lines[2]) // 2

        for i in range(0, no_of_goals * 2, 2):
            self.goals.append((int(lines[2][i]), int(lines[2][i + 1])))

        for i in range(3, number_of_walls + 3):
            self.walls.append((int(lines[i][0]), int(lines[i][1]), int(lines[i][2]), int(lines[i][3])))
        
        self.walls = self.find_wall_positions(self.walls)
        self.create_grid()

        for node in self.nodes:
            if node.square == self.starting_location:
                self.current_position = node

        file.close()

    def create_grid(self): #Create a NxN grid identifying where walls and goals are
        for i in range(self.rows):
            for x in range(self.columns):
                if (x, i) in self.walls:
                    self.nodes.append(Node(x, i, is_wall=True))
                elif (x, i) in self.goals:
                    self.nodes.append(Node(x, i, is_goal=True))
                else:
                    self.nodes.append(Node(x, i))
        
        for node in self.nodes:
            node.initialize_neighbours(self.nodes) #Initialize the neighbours for all the nodes
    
    def find_wall_positions(self, walls): #Used to find all the exact nodes of each wall given the format of (n, n, n, n)
        wall_coords = []
        for wall in walls:
            for i in range(wall[2]):
                for x in range(wall[3]):
                    wall_coords.append(((wall[0]) + i, wall[1] + x))
        
        return wall_coords
    
    def get_node_from_square(self, square): #Find a node instance based on the square coordinates of the parameter
        for node in self.nodes:
            if str(node.square) == str(square):
                return node
        return None

    def generate_graph(self): #Create a dictionary representing a graph, dictionary values are the coordinates of the neighbours of the key
        graph = {}
        valid_nodes = [node for node in self.nodes if node.is_wall == False] #Only add nodes as neighbours if they exist and they are not a wall

        for node in valid_nodes:
            graph[str(node.square)] = []
            for neighbour in node.neighbours.values():
                graph[str(node.square)].append(str(neighbour.square))
        
        return self.order_graph(graph, ['up', 'left', 'down', 'right'])
    
    def order_graph(self, graph, order): #Order graph by the dictionary values' position relative to the key
        for core_node, neighbours in graph.items(): 
            temp = [] #Set a temporary variable
            node = self.get_node_from_square(core_node)
            for direction in order:
                try:
                    if str(node.neighbours[direction].square) in neighbours:
                        temp.append(str(node.neighbours[direction].square))
                except KeyError:
                    pass
            graph[core_node] = temp #Change the graph value to the ordered temp variable
        return graph

    def convert_points_to_moves(self, path): #Convert a list of points to moves(i.e. (0, 1), (0, 2), (1, 2) becomes DOWN, RIGHT)
        path_moves = []
        for i in range(0, len(path) - 1):
            current_node = self.get_node_from_square(path[i])
            next_node = self.get_node_from_square(path[i + 1])
            for move, neighbour in current_node.neighbours.items():
                if next_node == neighbour:
                    path_moves.append(move)
                    
        return path_moves
    
    def cost_to_reach_goal(self, node, goal): #Uses the Manhattan Hueristic - The amount of squares between the goal and the node (inclusive of both)
        n = self.get_node_from_square(node)
        g = self.get_node_from_square(goal)

        x = abs(n.square[0] - g.square[0])
        y = abs(n.square[1] - g.square[1])
        
        return x + y
    
    def cost_to_move(self, node, origin_node = None): #An extra heuristic, where the cost to move if different for every action
        cost_to_move = 0

        if origin_node != None:
            origin_node = self.get_node_from_square(origin_node)

            #Costs are adjustable here:
            for move, neighbour in origin_node.neighbours.items():
                if str(neighbour.square) == node:
                    if move == 'down':
                        cost_to_move = 2
                    elif move == 'up':
                        cost_to_move = 2
                    elif move == 'left':
                        cost_to_move = 1
                    elif move == 'right':
                        cost_to_move = 1

        return cost_to_move
    
    def backtrace(self, parent, start, end): #Find the path to the goal by using the parents to backtrack to the start node from the end node
        path = [end]

        while path[-1] != start:
            path.append(parent[path[-1]]) #Add the parent of the path at the path list

        path.reverse()
        return path
    
    def depth_first_search(self, graph, starting_node, end_node):
        stack = [starting_node]
        visited = [starting_node]
        path = [starting_node]
        
        while stack: #Keeping looping until stack is empty
            next = stack.pop() #Remove the top most node from the stack to be examined
            if next == end_node:
                return [path, visited]
            for neighbour in graph[next]:
                if neighbour not in visited: #Add neighbours to lists if they are not already in this visited list
                    stack.append(neighbour)
                    visited.append(neighbour)
                    path.append(neighbour)
                    break

            if not stack: #Backtrack if stack is empty but there are still previous nodes with neighbours
                if len(path) > 1: 
                    stack.append(path[-2])
                    path.pop()
                else:
                    return [[], []] #If there are no more nodes return empty lists
    
    def breadth_first_search(self, graph, starting_node, end_node): #Foundation Code from GeeksForGeeks.com
        path_list = [[starting_node]]
        index = 0
        visited_nodes = [starting_node]
        
        if starting_node == end_node:
            return [[starting_node], [starting_node]]
            
        while index < len(path_list):
            current_path = path_list[index] #Find which path to change
            last_node = current_path[-1] 
            next_nodes = graph[last_node] #Neighbour nodes

            if end_node in next_nodes:
                current_path.append(end_node)
                return [current_path, visited_nodes]

            for next_node in next_nodes:
                if not next_node in visited_nodes: #Add neighbours to lists if they are not already in this visited list
                    new_path = current_path[:]
                    new_path.append(next_node)
                    path_list.append(new_path)
                    visited_nodes.append(next_node)

            index += 1 #Increase index

        return [[], []]
    
    def greedy_best_first_search(self, graph, starting_node, end_node):
        visited = []
        open_list = {}
        open_list[starting_node] = self.cost_to_reach_goal(starting_node, end_node) #Set heuristic of the starting node
        parent = {}
        found_path = False

        if starting_node == end_node:
            return [[starting_node], [starting_node]]

        while open_list:
            lowest_square = min(open_list, key = open_list.get) #Find square with the lowest heurstic value
            open_list.pop(lowest_square)
            visited.append(lowest_square)

            if lowest_square == end_node:
                found_path = True
                break #End loop if path has been completed
            
            for neighbour in graph[lowest_square]:
                if neighbour not in visited:
                    open_list[neighbour] = self.cost_to_reach_goal(neighbour, end_node) #Set heuristic to the manhattan distance from the start to the goal node
                    if neighbour not in parent: #Only add to parent dictionary if neighbour is not already in
                        parent[neighbour] = lowest_square

        if found_path == True:
            return [self.backtrace(parent, starting_node, end_node), visited] #Back track using the nodes' parents to find a path
        else:
            return [[], []]
    
    def a_star_search(self, graph, starting_node, end_node):
        visited = []
        open_list = {}
        open_list[starting_node] = self.cost_to_reach_goal(starting_node, end_node)
        parent = {}
        found_path = False

        if starting_node == end_node:
            return [[starting_node], [starting_node]]

        while open_list:
            lowest_square = min(open_list, key = open_list.get)
            open_list.pop(lowest_square)
            visited.append(lowest_square)

            if lowest_square == end_node:
                found_path = True
                break
            
            for neighbour in graph[lowest_square]:
                if neighbour not in visited:
                    open_list[neighbour] = self.cost_to_reach_goal(neighbour, end_node) + self.cost_to_move(neighbour, lowest_square)#Set heuristic to the manhattan distance from the start to the goal node + the cost to move UP/DOWN/LEFT/RIGHT
                    if neighbour not in parent: 
                        parent[neighbour] = lowest_square

        if found_path == True:
            return [self.backtrace(parent, starting_node, end_node), visited]
        else:
            return [[], []]

    def custom_search_1(self, graph, starting_node, end_node):
        graph = self.order_graph(graph, ['right', 'left', 'down', 'up']) #Change the order of precedence when moving
        return self.depth_first_search(graph, starting_node, end_node) #Complete a Depth First search with a new order
    
    def custom_search_2(self, graph, starting_node, end_node):
        visited = []
        open_list = {}
        open_list[starting_node] = self.cost_to_reach_goal(starting_node, end_node)
        parent = {}
        found_path = False

        if starting_node == end_node:
            return [[starting_node], [starting_node]]

        while open_list:
            second_lowest_square = None
            lowest_square = min(open_list, key = open_list.get)
            open_list.pop(lowest_square)
            visited.append(lowest_square)

            if lowest_square == end_node:
                found_path = True
                break

            if len(open_list) > 0: #If the list is not already empty, find the square with the lowest value after the previous loewst value was removed from the list
                second_lowest_square = min(open_list, key = open_list.get)
                open_list.pop(second_lowest_square)
                visited.append(second_lowest_square)

                if second_lowest_square == end_node:
                    found_path = True
                    break
            
            for neighbour in graph[lowest_square]: #Search through the neighbours of the lowest square node
                if neighbour not in visited:
                    open_list[neighbour] = self.cost_to_reach_goal(neighbour, end_node) #Uses the Manhattan heursitic liek GBFS
                    if neighbour not in parent:
                        parent[neighbour] = lowest_square

            if second_lowest_square != None: #Do the same with second lowest square node
                for neighbour in graph[second_lowest_square]:
                    if neighbour not in visited:
                        open_list[neighbour] = self.cost_to_reach_goal(neighbour, end_node)
                        if neighbour not in parent:
                            parent[neighbour] = second_lowest_square
        
        if found_path == True:
            return [self.backtrace(parent, starting_node, end_node), visited]
        else:
            return [[], []]
    
    def search_stats(self, method, goal): #Given a method, print out the results of the search
        path = []
        no_of_visited = 0
        if method.lower() == 'bfs':
            x = self.breadth_first_search(self.generate_graph(), str(self.starting_location), str(goal))
            path = x[0] #Set path to the first returned value
            no_of_visited = len(x[1]) #Set the number of visited to the length of visited (the second returned value)
        elif method.lower() == 'dfs':
            x = self.depth_first_search(self.generate_graph(), str(self.starting_location), str(goal))
            path = x[0]
            no_of_visited = len(x[1])
        elif method.lower() == 'gbfs':
            x = self.greedy_best_first_search(self.generate_graph(), str(self.starting_location), str(goal))
            path = x[0]
            no_of_visited = len(x[1])
        elif method.lower() == 'as':
            x = self.a_star_search(self.generate_graph(), str(self.starting_location), str(goal))
            path = x[0]
            no_of_visited = len(x[1])
        elif method.lower() == 'cus1':
            x = self.custom_search_1(self.generate_graph(), str(self.starting_location), str(goal))
            path = x[0]
            no_of_visited = len(x[1])
        elif method.lower() == 'cus2':
            x = self.custom_search_2(self.generate_graph(), str(self.starting_location), str(goal))
            path = x[0]
            no_of_visited = len(x[1])

        if len(path) < 1:
            print('Could not find path')
        elif len(path) == 1:
            print('You are already in this position')
        else:
            print(', '.join(self.convert_points_to_moves(path))) #Convert the paths to moves (such as up and down)
            print('Number of visited nodes: ' + str(no_of_visited) + '\n') #Print the number of visited
    
    def shortest_path_to_all_goals(self, starting_node, goals): #
        directions = []
        source = starting_node

        while goals:
            goals.sort(key=lambda x : self.cost_to_reach_goal(source, x)) #Lambda function that sorts the goals by how far they are from a given source

            end = goals[0]
            search = self.breadth_first_search(self.generate_graph(), str(source), str(end)) #Complete a single BFS to the closest goal
            if search[0] == []:
                return None #return nothing if BFS returns an empty list
            source = search[0][-1] #Change the source to the last node in the path
            goals.remove(end)#Remove the goal from the list once it has been reached
            directions.extend(self.convert_points_to_moves(search[0])) #Extend the directions to include paths from multiple BFS searches

        return directions #return the directions which cover all the goals

if __name__ == '__main__':
    robot = Robot() 
    robot.read_from_file('data.txt')