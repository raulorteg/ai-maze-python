# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 00:01:40 2020
@author: Raul Ortega Ochoa
"""
import pygame
import csv
from time import sleep
from helper_maze_generator import generate_step

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


# initialize the grid array full of zeros
grid = []
num_rows = 41
num_columns = num_rows
for row in range(num_rows):
    grid.append([])
    for column in range(num_columns):
        grid[row].append(0)

# # load the pattern that was pre-written in helpers.py
# load_pattern(grid)

# initialize pygame
pygame.init()

# congiguration of the window
WINDOW_SIZE = [330, 330]
screen = pygame.display.set_mode(WINDOW_SIZE)
# screen title
pygame.display.set_caption("Generating Maze ...")
 

# loop until done
done = False
# when run = True start running the algorithm
run = False

clock = pygame.time.Clock() # to manage how fast the screen updates

# initialize last_pos variable. Its the starting point for the algorithm
last_pos = (0, 0)
pos_history = []
pos_history.append(last_pos)

back_step = 0

# define start and goal
grid[0][0] = 2
grid[-1][-1] = 3

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
    
    for row in range(num_rows):
        for column in range(num_columns):
            # color = white
            if grid[row][column] == 1:
                color = white
                pygame.draw.rect(screen, color, 
                                 [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width,
                                  height])
            elif grid[row][column] == 2:
                color = green
                pygame.draw.rect(screen, color,
                                 [(margin + width) * column + margin,
                                  (margin + height) * row + margin,
                                  width,
                                  height])
            elif grid[row][column] == 3:
                color = red
                pygame.draw.rect(screen, color,
                                 [(margin + width) * column + margin,
                                  (margin + height) * row + margin,
                                  width,
                                  height])
            elif grid[row][column] == 4:
                color = blue
                pygame.draw.rect(screen, color,
                                 [(margin + width) * column + margin,
                                  (margin + height) * row + margin,
                                  width,
                                  height])
            else:
                color = black
                pygame.draw.rect(screen, color, 
                                 [(margin + width) * column + margin, 
                                  (margin + height) * row + margin,
                                  width,
                                  height])
    
    
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
        # wait for user to press any key to start    
        if event.type == pygame.KEYDOWN:
            close = True
pygame.quit() # so that it doesnt "hang" on exit

# # export maze to .csv file
# with open("mazes/maze.csv", "w", newline="") as f:
#     writer = csv.writer(f)
#     writer.writerows(grid)