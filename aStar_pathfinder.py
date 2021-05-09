# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:51:53 2020
@author: Raul Ortega Ochoa
"""
import pygame, time, csv, argparse
import numpy as np
from time import sleep
from helper_aStar import generate_step, pick_node_from_list, Node

if __name__ == "__main__":

  start_t0 = time.time()

  # parsing user input
  # example: python aStar_generator.py --display=True --maze_file=maze_1.csv
  parser = argparse.ArgumentParser()
  parser.add_argument("--display", help="Display generating process 0: False, 1:True", default=1, type=int)
  parser.add_argument("--maze_file", help="filename (csv) of the maze to load.", default="maze_1.csv", type=str)
  args = parser.parse_args()

  address = "mazes/" + args.maze_file
  grid = np.genfromtxt(address, delimiter=',', dtype=int)

  # define goal and start
  num_rows = len(grid)
  num_columns = len(grid[0])
  goal = (num_rows-1, num_columns-1)
  start = (0,0)

  # define start node
  start_node = Node(None, 0, start)

  # initialize seen, frontier list
  seen = [] # starts empty
  frontier = [start_node] # starts with the start node


  if args.display == 1:

    # define colors of the grid RGB
    black = (0, 0, 0) # grid == 0
    white = (255, 255, 255) # grid == 1
    green = (50,205,50) # grid == 2
    red = (255,99,71) # grid == 3
    grey = (211,211,211) # for background
    blue = (153,255,255) # grid == 4, where current position is
    magenta = (255,0,255) # grid == 5 solution

    # set the height/width of each location on the grid
    height = 7
    width = height # i want the grid square
    margin = 1 # sets margin between grid locations

    # initialize pygame
    pygame.init()

    # congiguration of the window
    WINDOW_SIZE = [330, 330]
    screen = pygame.display.set_mode(WINDOW_SIZE)

    pygame.display.set_caption(f"A* Pathfinder. Solving: {address}")
    clock = pygame.time.Clock() # to manage how fast the screen updates

    idx_to_color = [black, white, green, red, blue, magenta]

    # loop until done
    interrupt = False # when user clicks exit
    run = False # when algorithm starts
    finish = False
    last_iter = False

    # main painting loop
    while not interrupt:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                interrupt = True
                
            # wait for user to press RETURN key to start    
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_RETURN:
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
        
        if last_iter == True:
            interrupt = True
            run = False
        elif run == True:
            
            # pick a node from the frontier
            current_node = pick_node_from_list(frontier)
            grid, frontier, seen, current_node = generate_step(grid, frontier, seen, current_node)

            if current_node.position == goal: # if ai is at goal then finish
                last_iter = True
                ### follow the parents back to the origin
                while current_node.parent != None:
                    x, y = current_node.position
                    grid[x,y] = 5
                    current_node = current_node.parent
             
            sleep(0.01) # control speed of the update
        
    while not finish:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            # wait for user to press any key to start    
            elif event.type == pygame.KEYDOWN:
                finish = True
    pygame.quit() # so that it doesnt "hang" on exit

  else:

    print(f"A* Pathfinder. Solving: {address}")

    done = False
    while not done:
        
      # pick a node from the frontier
      current_node = pick_node_from_list(frontier)
      grid, frontier, seen, current_node = generate_step(grid, frontier, seen, current_node)

      if current_node.position == goal: # if ai is at goal then finish
        done = True
        # follow the parents back to the origin
        while current_node.parent != None:
          x, y = current_node.position
          grid[x,y] = 5
          current_node = current_node.parent

  # export maze to .csv file
  with open(f"mazes_solutions/aStar_{args.maze_file}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerows(grid)

  print(f"--- finished {time.time()-start_t0:.3f} s---")
  exit(0)