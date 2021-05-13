# -*- coding: utf-8 -*-
"""
@author: Raul Ortega
"""
import pygame, time, argparse, csv
import numpy as np
from time import sleep
from numpy.random import randint

def is_in_map(pos, grid_dim):
    """
    Parameters
    ----------
    pos : tuple of 2 ints 
        x, y coordinates in the grid system of current
        position
    grid_dim : tuple of ints
        x, y dimension of the grid system
    Returns
        true if pos in map
        false if not in map
    """
    (max_x, max_y) = grid_dim # unroll the dimensions
    (x, y) = pos # unroll the position coordinates
    
    x_in = (x <= max_x) & (x >= 0) # logical x in map
    y_in = (y <= max_y) & (y >= 0) # logical y in map
    return bool(x_in*y_in) # only true if both true

class Node:
    def __init__(self, pos, parent):
        self.x = pos[0]
        self.y = pos[1]
        self.parent = parent

    def __getitem__(self):
          return (self.x, self.y)

    def position(self):
        return (self.x, self.y)


class Queue:
    def __init__(self):
        self.Queue = []

    def __len__(self):
        return len(Queue)

    def append(self, node):
        self.Queue.append(node)

    def get_node(self):
        return self.Queue[0]

    def get_node_position(self):
        node = self.Queue[0]
        return node.position()

    def remove(self):
        self.Queue = self.Queue[1:len(self.Queue)]

class BFS:
    def __init__(self, start_pos, goal_pos, grid_dim):
        self.grid_dim = grid_dim
        self.start_pos = start_pos
        self.goal_pos = goal_pos
        self.explored = Queue()
        self.frontier = Queue()
        node = Node(pos=start_pos, parent=None)
        self.frontier.append(node)

    def backtrack_solution(self, grid, curr_node):
        solution = []
        while curr_node.parent != None:
            solution.append(curr_node.position())
            curr_node = curr_node.parent

        return solution

    def compute_successors(self, grid):
        curr_node = self.frontier.get_node()
        x, y = curr_node.position()

        for movement in [(1,0), (-1,0), (0,1), (0,-1)]:
            dx, dy = movement
            new_pos = (x+dx, y+dy)

            if (is_in_map(new_pos, self.grid_dim)) and (grid[new_pos[0], new_pos[1]] in [1, 3]) :
                new_node = Node(pos=new_pos, parent=curr_node)
                self.frontier.Queue.append(new_node)

                if set(new_pos) == set(goal_pos):
                    self.explored.append(self.frontier.get_node())
                    self.frontier.remove()
                    done = True
                    solution = self.backtrack_solution(grid, curr_node=new_node)
                    return solution, done

        self.explored.Queue.append(curr_node)
        self.frontier.remove()
        done = False
        return [], done


if __name__ == "__main__":
  start_t0 = time.time()

  # parsing user input
  # example: python bfs_pathfinder.py --display=True --maze_file=maze_1.csv
  parser = argparse.ArgumentParser()
  parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
  parser.add_argument("--maze_file", help="filename (csv) of the maze to load.", default="maze_1.csv", type=str)
  args = parser.parse_args()

  address = "mazes/" + args.maze_file
  grid = np.genfromtxt(address, delimiter=',', dtype=int)
  num_rows = len(grid)
  num_columns = len(grid[0])

  # define start, define goal
  start_pos = (0,0)
  goal_pos = (num_rows-1, num_columns-1)

  # define start and goal
  grid[0, 0] = 2
  grid[-1, -1] = 3

  grid_dim = (num_rows-1, num_columns-1)

  if args.display == 1:
    # define the two colors of the grid RGB
    black = (0,0,0)
    white = (255, 255, 255)
    green = (50,205,50)
    red = (255,99,71)
    grey = (211,211,211)
    blue = (153,255,255)
    magenta = (255,0,255)

    idx_to_color = [black, white, green, red, blue, magenta]

    # set the height/width of each location on the grid
    height = 7
    width = height # i want the grid square
    margin = 1 # sets margin between grid locations

    # initialize pygame
    pygame.init()

    # congiguration of the window
    WINDOW_SIZE = [330, 330]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption(f"BFS Pathfinder. Solving: {address}")

    # loop until done
    done = False
    run = False
    close = False

    clock = pygame.time.Clock() # to manage how fast the screen updates

    bfs = BFS(start_pos=start_pos, goal_pos=goal_pos, grid_dim=grid_dim)

    # main program
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            # wait for user to press any key to start    
            elif event.type == pygame.KEYDOWN:
                run = True
        
        screen.fill(grey) # fill background in grey
        
        for row in range(num_rows):
            for column in range(num_columns):
                color = idx_to_color[grid[row, column]]
                pygame.draw.rect(screen, color, 
                                  [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width, height])
        
        
        clock.tick(60) # set limit to 60 frames per second
        pygame.display.flip() # update screen
        
        if run == True:

            sleep(0.01)
            solution, done = bfs.compute_successors(grid=grid)
        
            explored = [node.position() for node in bfs.explored.Queue]

            for pos in explored:
                grid[pos[0], pos[1]] = 4

        if done == True:
            for pos in solution:
                grid[pos[0], pos[1]] = 5

            grid[0, 0] = 2
            grid[-1, -1] = 3

            screen.fill(grey) # fill background in grey
        
            for row in range(num_rows):
                for column in range(num_columns):
                    color = idx_to_color[grid[row, column]]
                    pygame.draw.rect(screen, color, 
                                      [(margin + width) * column + margin, 
                                      (margin + height) * row + margin,
                                      width, height])
        
        
            clock.tick(60) # set limit to 60 frames per second
            pygame.display.flip() # update screen

            
    print("Solved! Click exit.")
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            # wait for user to press any key to start    
            elif event.type == pygame.KEYDOWN:
                close = True
    pygame.quit()

  else:
    print(f"Pathfinder BFS. solving: {address}")

    # loop until done
    done = False
    bfs = BFS(start_pos=start_pos, goal_pos=goal_pos, grid_dim=grid_dim)

    # main program
    while not done:
        solution, done = bfs.compute_successors(grid=grid)

        explored = [node.position() for node in bfs.explored.Queue]

        for pos in explored:
            grid[pos[0], pos[1]] = 4

    # lets save result in csv
    for pos in solution:
        grid[pos[0], pos[1]] = 5

    grid[0, 0] = 2
    grid[-1, -1] = 3


  # export maze to .csv file
  with open(f"mazes_solutions/bfs_{args.maze_file}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(grid)

  print(f"--- finished {time.time()-start_t0:.3f} s---")
  exit(0)