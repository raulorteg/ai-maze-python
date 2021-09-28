# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:51:53 2020
@author: Raul Ortega Ochoa
"""
import pygame, csv
import numpy as np

class Node: # define a Node class
    def __init__(self, parent, cost, position):
        self.parent = parent
        self.cost = cost
        self.position = position

class aStar:
    def __init__(self, map_address: str, display: bool = False, save_solution: bool = False):
        """
        :param map_address: string path to the map that wants to be loaded.
        :type map_address: string

        :param display: boolean flag to set the display mode. (Deafult False)
        :type display: bool

        :param save_solution: boolean flag to set option to save the solved maze. (Deafult False)
        :type save_solution: bool
        """
        self.map_address = map_address
        self.display = display # TODO:
        self.save_solution = save_solution

        self.__load_grid()

        self.seen = []
        self.start_node = Node(None, 0, (0,0))
        self.frontier = [self.start_node]
        self.finished = False
    
    def __load_grid(self):
        """ hidden method loads the map from the path :map_address:"""
        try:
            grid = np.genfromtxt(self.map_address, delimiter=',', dtype=int)
        except:
            raise Exception("Couldn't locate the map at {}".format(self.map_address))
        
        self.grid = grid
        self.dim_grid = (grid.shape[0]-1, grid.shape[1]-1)
        self.goal_coord = self.dim_grid
    
    def __remove_node_frontier(self, node):
        pos = node.position
        new_frontier = []
        for item in self.frontier:
            if item.position != pos:
                new_frontier.append(item)
        self.frontier = new_frontier


    def __is_in_map(self, pos):
        (max_x, max_y) = self.dim_grid # unroll the dimensions
        (x, y) = pos # unroll the position coordinates
        
        x_in = (x <= max_x) & (x >= 0) # logical x in map
        y_in = (y <= max_y) & (y >= 0) # logical y in map
        return bool(x_in*y_in) # only true if both true

    def compute_node_cost(self, pos):
        x, y = pos
        x_goal, y_goal = self.goal_coord
        cost = np.sqrt((x_goal-x)**2 + (y_goal-y)**2)
        return cost

    def compute_successors(self, current_node):

        movements = [(1,0), (-1,0), (0,1), (0,-1)]
        x_0, y_0 = current_node.position
                
        successors = []
        for movement in movements:
            dx, dy = (movement[0], movement[1])
            next_pos = (x_0+dx, y_0+dy)
            cond1 = self.__is_in_map(next_pos) # if its on the map
            if cond1:
                cond2 = self.grid[next_pos[0], next_pos[1]] != 0 # if not wall
                cond3 = next_pos not in [item.position for item in self.seen] # dont go to any already seen
                if bool(cond2*cond3):
                    cost = self.compute_node_cost(next_pos)
                    new_node = Node(current_node, cost, next_pos)
                    successors.append(new_node)
        return successors

    def __pick_node_from_list(self, node_list):
        if len(node_list) == 1:
            current_node = node_list[0]
            return current_node
        
        current_node = Node(None, np.inf, (0,0)) # initialize current node
        for node in node_list:
            if node.cost < current_node.cost: # pick up the node with least cost
                current_node = node
        return current_node

    def generate_step(self, current_node):

        self.seen.append(current_node) # add parent to seen list

        successors = self.compute_successors(current_node) # given the node compute the successors
        self.__remove_node_frontier(current_node) # remove parent from frontier
        for son in successors:
            self.frontier.append(son) # add successors to the frontier
        
        current_node = self.__pick_node_from_list(successors) # pick one of the successors

        x, y = current_node.position # paint the grid with the new node position
        self.grid[x, y] = 4 # paint blue
        
        return self.grid, self.frontier, self.seen, current_node

    def run(self):
        while not self.finished:
            current_node = self.__pick_node_from_list(self.frontier)
            self.__remove_node_frontier(current_node)
            _, _, _, current_node = self.generate_step(current_node)

            if current_node.position == self.goal_coord:
                self.finished = True
                ### follow the parents back to the origin
                while current_node.parent != None:
                    x, y = current_node.position
                    self.grid[x,y] = 5
                    current_node = current_node.parent
        
        if self.save_solution:
            # export maze to .csv file
            with open(f"../mazes_solutions/aStar_{args.maze_file}", "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(self.grid)


if __name__ == "__main__":
    import time, argparse
    from time import sleep

    start_t0 = time.time()

    # parsing user input
    # example: python aStar.py --display=True --maze_file=maze_1.csv
    parser = argparse.ArgumentParser()
    parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
    parser.add_argument("--maze_file", help="filename (csv) of the maze to load.", default="maze_1.csv", type=str)
    args = parser.parse_args()

    address = "../mazes/" + args.maze_file

    # Create the agent
    agent = aStar(map_address=address)
    agent.run()

    print(f"--- finished {time.time()-start_t0:.3f} s---")