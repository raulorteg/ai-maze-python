# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:51:53 2020

@author: Raul Ortega Ochoa
"""
import pygame
from time import sleep
from helper_ai_pathfinder import load_maze, generate_step, pick_node_from_list

class Node: # define a Node class
    def __init__(self, parent, cost, position):
        self.parent = parent
        self.cost = cost
        self.position = position

# # ask user for path to maze
# address = input("Path to maze: ")

address = "mazes/maze3.csv"
grid = load_maze(address)

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

# =======================================================
# SETTINGS FOR PYGAME

# define colors of the grid RGB
black = (0, 0, 0) # grid == 0
white = (255, 255, 255) # grid == 1
green = (50,205,50) # grid == 2
red = (255,99,71) # grid == 3
grey = (211,211,211) # for background
blue = (153,255,255) # grid[x][y] == 4, where current position is
magenta = (255,0,255) # grid[x][y] == 5 solution
# set the height/width of each location on the grid
height = 7
width = height # i want the grid square
margin = 1 # sets margin between grid locations

# initialize pygame
pygame.init()

# congiguration of the window
WINDOW_SIZE = [600, 600]
screen = pygame.display.set_mode(WINDOW_SIZE)
# screen title
pygame.display.set_caption(f"Pathfinder. {address}")

clock = pygame.time.Clock() # to manage how fast the screen updates

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
            
        # wait for user to press any key to start    
        elif event.type == pygame.KEYDOWN:
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
            elif grid[row][column] == 5:
                color = magenta
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
    
    if last_iter == True:
        interrupt = True
        run = False
    elif run == True:
        
        # pick a node from the frontier
        current_node = pick_node_from_list(frontier)
        grid, frontier, seen, current_node = generate_step(grid, frontier, seen, current_node)
        print(f"AI is at {current_node.position}")
        if current_node.position == goal: # if ai is at goal then finish
            last_iter = True
            ### TODO: follow the parents back to the origin
            while current_node.parent != None:
                x, y = current_node.position
                grid[x][y] = 5
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

