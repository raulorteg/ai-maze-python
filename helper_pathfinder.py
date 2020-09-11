# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 10:22:53 2020

@author: Raul Ortega Ochoa
"""
import csv
from numpy.random import randint

def load_maze(address):
    """
    Parameters
    ----------
    address : string format "mazes/maze1.csv"
        Address of where to find the maze to import.

    Returns
    grid : list of lists, returns the maze itself (grid)
    """
    grid = []
    with open(address, "r", newline="") as f:
            reader = csv.reader(f)
            for row in reader:
                grid.append(row)
                
    # convert to ints
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            grid[i][j] = int(grid[i][j])
    return grid

# =========================================

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
        if (grid[x][y] == 3): # if red
            valid_steps = []
            valid_steps.append(possible_step)
            done = True
            return grid, last_pos, back_step, done
        
        elif (grid[x][y] == 1): # if white
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
        grid[x][y] = 4 # paint blue
        done = False
        return grid, last_pos, back_step, done
    
    else:
        back_step = 0
        index = randint(0, len(valid_steps))
        last_pos = valid_steps[index]
        x, y = last_pos
        grid[x][y] = 4 # paint blue
        done = False
        return grid, last_pos, back_step, done
    
