# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 10:16:38 2020

@author: Raul Ortega Ochoa
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

# ===========================

def possible_next_steps(grid_dim, last_pos):
    """
    Parameters
    ----------
    grid_dim : tuple of 2 ints
        dimensions of the grid
    last_pos : tuple of 2 ints
        x, y coordinates of current position
    Returns
        possible_steps: list of list of tuples (x,y) denoting the
        next 2 movements possible in every direction possible
    """
    x, y = last_pos
    movements = [(1,0), (-1,0), (0,1), (0,-1)]
    possible_steps = []
    for movement in movements:
        dx, dy = movement
        next_mov = (x+dx, y+dy)
        if is_in_map(next_mov, grid_dim):
            possible_steps.append(next_mov)
        
    return possible_steps

def generate_step(grid, last_pos, pos_history, back_step):
    """
    Parameters
    ----------
    grid : list of list of ints
        the grid, it is filled with 0, 1, 2, 3 that correspond
        to different colors
    last_pos : tuple of 2 ints
        x, y coordinates of current position
    pos_history : list of tuples of 2 ints
        coordinates of last visited nodes, only add when see for the
        first time
    Returns
        changes grid[x][y] to white through the path the algorithm is going
        and paints the last_pos on the grid blue
        returns grid, last_pos, back_step, done
    """
    x, y = last_pos
    grid_dim = (len(grid)-1, len(grid[0])-1)
    possible_steps = possible_next_steps(grid_dim, last_pos)
    
    valid_steps = []
    for possible_step in possible_steps:
        x, y = possible_step
        if (grid[x,y] == 3): # if red
            valid_steps = []
            valid_steps.append(possible_step)
            done = True
            return grid, last_pos, back_step, done
        
        elif (grid[x,y] == 1): # if white
            valid_steps.append(possible_step)
            
    if len(valid_steps) == 0:
        last_pos = pos_history[-1-back_step]
        back_step += 1
        done = False
        return grid, last_pos, back_step, done
    
    elif len(valid_steps) == 1:
        back_step = 0
        x, y = valid_steps[0]
        last_pos = (x, y)
        grid[x,y] = 4 # paint blue
        done = False
        return grid, last_pos, back_step, done
    
    else:
        back_step = 0
        index = randint(0, len(valid_steps))
        last_pos = valid_steps[index]
        x, y = last_pos
        grid[x,y] = 4 # paint blue
        done = False
        return grid, last_pos, back_step, done


if __name__ == "__main__":
  start_t0 = time.time()

  # parsing user input
  # example: python dfs_generator.py --display=True --maze_file=maze_1.csv
  parser = argparse.ArgumentParser()
  parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
  parser.add_argument("--maze_file", help="filename (csv) of the maze to load.", default="maze_1.csv", type=str)
  args = parser.parse_args()

  address = "mazes/" + args.maze_file
  grid = np.genfromtxt(address, delimiter=',', dtype=int)
  num_rows = len(grid)
  num_columns = len(grid[0])

  # define start, define goal
  start = (0,0)
  last_pos = (0,0)
  goal = (num_rows-1, num_columns-1)
  pos_history = []
  pos_history.append(last_pos)
  back_step=0

  # define the two colors of the grid RGB
  black = (0, 0, 0) # grid == 0
  white = (255, 255, 255) # grid == 1
  green = (50,205,50) # grid == 2
  red = (255,99,71) # grid == 3
  grey = (211,211,211) # for background
  blue = (153,255,255) # grid[x][y] == 4, where current position is

  # set the height/width of each location on the grid
  height = 7
  width = height # i want the grid square
  margin = 1 # sets margin between grid locations

  # define start and goal
  grid[0, 0] = 2
  grid[-1, -1] = 3

  if args.display == 1:
    # initialize pygame
    pygame.init()

    # congiguration of the window
    WINDOW_SIZE = [330, 330]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption(f"Pathfinder. {address}")

    idx_to_color = [black, white, green, red, blue]

    # loop until done
    done = False
    run = False
    close = False

    clock = pygame.time.Clock() # to manage how fast the screen updates

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
        
        # set limit to 60 frames per second
        clock.tick(60)
        
        # update screen
        pygame.display.flip()
        
        if run == True:
            # feed the algorithm the last updated position and the grid
            grid, last_pos, back_step, done = generate_step(grid, last_pos, pos_history, back_step)
            if last_pos not in pos_history:
                pos_history.append(last_pos)
            sleep(0.01)
        
    while not close:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close = True
            # wait for user to press any key to start    
            elif event.type == pygame.KEYDOWN:
                close = True
    pygame.quit()

  else:
    print(f"Pathfinder DFS. solving: {address}")

    # loop until done
    done = False

    # main program
    while not done:
        # feed the algorithm the last updated position and the grid
        grid, last_pos, back_step, done = generate_step(grid, last_pos, pos_history, back_step)
        if last_pos not in pos_history:
              pos_history.append(last_pos)

  # export maze to .csv file
  with open(f"mazes_solutions/dfs_{args.maze_file}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(grid)

  print(f"--- finished {time.time()-start_t0:.3f} s---")
  exit(0)