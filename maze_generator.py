# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 00:01:40 2020
@author: Raul Ortega Ochoa
"""
import pygame, argparse, csv, time
import argparse
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
    x_pos, y_pos = last_pos # unroll coordinates
    
    possible_steps = []
    operations_1 = [(0,1), (0,-1), (1,0), (-1,0)]
    operations_2 = [(0,2), (0,-2), (2,0), (-2,0)]
    num_operations = len(operations_1)
    
    for i in range(num_operations):
        op1_x, op1_y = operations_1[i]
        op2_x, op2_y = operations_2[i]
        
        if (is_in_map((x_pos + op1_x, y_pos + op1_y), grid_dim)) and (is_in_map((x_pos + op2_x, y_pos + op2_y), grid_dim)):
            possible_steps.append([(x_pos + op1_x, y_pos + op1_y), (x_pos + op2_x, y_pos + op2_y)])
    return possible_steps
# ===========================
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
    (x, y) = last_pos
    grid[x, y] = 1
    
    grid_dim = (len(grid), len(grid[0]))
    possible_steps = possible_next_steps(grid_dim, last_pos)
    
    valid_steps = []
    for step in possible_steps:
        (x1, y1) = step[0]
        (x2, y2) = step[1]
        
        not_white = (grid[x1, y1] != 1) & (grid[x2, y2] != 1)
        not_green = (grid[x1, y1] != 2) & (grid[x2, y2] != 2)
        
        if bool(not_white * not_green):
            valid_steps.append(step)
    
    #print(f"Valid steps: {valid_steps}")
    
    if (len(valid_steps) == 0): # if it is a dead end
        last_pos = pos_history[-2 - back_step]
        if last_pos == (0,0):
            done = True
            return grid, last_pos, back_step, done
        back_step += 1
        done = False
        return grid, last_pos, back_step, done
    
    else:
        back_step = 0 # reset it
        # choose a valid step at random
        if (len(valid_steps) == 1):
            last_pos = valid_steps[0]
            (x1, y1) = last_pos[0]
            (x2, y2) = last_pos[1]
            grid[x1, y1] = 1
            grid[x2, y2] = 4
            last_pos = last_pos[1]
            done = False
            return grid, last_pos, back_step, done
        else:
            index = randint(0, len(valid_steps))
            # print(f"valid: {len(valid_steps)}, chose {index}")
            last_pos = valid_steps[index]
            (x1, y1) = last_pos[0]
            (x2, y2) = last_pos[1]
            grid[x1, y1] = 1
            grid[x2, y2] = 4
            last_pos = last_pos[1]
            done = False
            return grid, last_pos, back_step, done
#==============================================================================
#==============================================================================

if __name__ == "__main__":

  start_t0 = time.time()

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

  # parsing user input
  # example: python maze_generator.py --display=True --num_mazes=1
  parser = argparse.ArgumentParser()
  parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
  parser.add_argument("--num_mazes", help="Number of mazes to generate.", default=1, type=int)
  args = parser.parse_args()

  for iter_maze in range(args.num_mazes):
    start_t = time.time()

    # initialize the grid array full of zeros
    num_rows = 41
    num_columns = num_rows
    grid = np.zeros((num_rows, num_columns))

    if args.display == 1:
      # initialize pygame
      pygame.init()

      # congiguration of the window
      WINDOW_SIZE = [330, 330]
      screen = pygame.display.set_mode(WINDOW_SIZE)
      # screen title
      pygame.display.set_caption(f"Generating Maze {iter_maze+1}/{args.num_mazes}...")

      done = False # loop until done
      run = False # when run = True start running the algorithm

      clock = pygame.time.Clock() # to manage how fast the screen updates

      idx_to_color = [black, white, green, red, blue]

      # initialize last_pos variable. Its the starting point for the algorithm
      last_pos = (0, 0)
      pos_history = []
      pos_history.append(last_pos)
      back_step = 0

      # define start and goal
      grid[0, 0] = 2
      grid[-1, -1] = 3

      # main program
      while not done:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            done = True
              
          # wait for user to press RETURN key to start    
          elif event.type == pygame.KEYDOWN:
              if event.key==pygame.K_RETURN:
                  run = True
      
        screen.fill(grey) # fill background in grey
        
        # draw
        for row in range(num_rows):
          for column in range(num_columns):

            color = idx_to_color[int(grid[row, column])]
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

      close = False
      while not close:
        for event in pygame.event.get():
          if event.type == pygame.QUIT:
            close = True
            pygame.quit()
        # wait for user to press any key to start    
        if event.type == pygame.KEYDOWN:
            close = True
            pygame.quit()

    else:

      print(f"Generating Maze {iter_maze}/{args.num_mazes}...", end=" ")

      done = False # loop until done

      # initialize last_pos variable. Its the starting point for the algorithm
      last_pos = (0, 0)
      pos_history = []
      pos_history.append(last_pos)
      back_step = 0

      # define start and goal
      grid[0, 0] = 2
      grid[-1, -1] = 3

      # main program
      while not done:
        # feed the algorithm the last updated position and the grid
        grid, last_pos, back_step, done = generate_step(grid, last_pos, pos_history, back_step)
        if last_pos not in pos_history:
          pos_history.append(last_pos)

    # export maze to .csv file
    with open(f"mazes/maze_{iter_maze}.csv", "w", newline="") as f:
      writer = csv.writer(f)
      writer.writerows(grid)
    print(f"{time.time()-start_t:.3f} s")

  print(f"--- finished {time.time()-start_t0:.3f} s---")
  exit(0)