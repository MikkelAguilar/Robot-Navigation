class Node:
    def __init__(self, x, y, is_wall = False, is_goal = False):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.is_goal = is_goal
        self.visited = False
        self.square = (x, y)
        self.neighbours = {}
    
    def initialize_neighbours(self, all_nodes): #Find all the neighbours of the node
        self.neighbours = {}
        for node in all_nodes:
            if node.square == (self.x + 1, self.y) and node.is_wall == False and node.visited == False: #Node is not a neighbour if it has been visited or it is a wall
                self.neighbours['right'] = node
            elif node.square == (self.x - 1, self.y) and node.is_wall == False and node.visited == False:
                self.neighbours['left'] = node
            elif node.square == (self.x, self.y + 1) and node.is_wall == False and node.visited == False: 
                self.neighbours['down'] = node
            elif node.square == (self.x, self.y - 1) and node.is_wall == False and node.visited == False:
                self.neighbours['up'] = node