
"""
Created on Wed Sep  9 15:03:29 2020

@author: Raul Ortega Ochoa
"""
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
    grid[x][y] = 1
    
    grid_dim = (len(grid), len(grid[0]))
    possible_steps = possible_next_steps(grid_dim, last_pos)
    #print(f"Position: {last_pos}")
    #print(f"Possible steps: {possible_steps}")
    
    valid_steps = []
    for step in possible_steps:
        (x1, y1) = step[0]
        (x2, y2) = step[1]
        
        not_white = (grid[x1][y1] != 1) & (grid[x2][y2] != 1)
        not_green = (grid[x1][y1] != 2) & (grid[x2][y2] != 2)
        
        if bool(not_white * not_green):
            valid_steps.append(step)
    
    #print(f"Valid steps: {valid_steps}")
    
    if (len(valid_steps) == 0): # if it is a dead end
        last_pos = pos_history[-2 - back_step]
        if last_pos == (0,0):
            print("finished")
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
            grid[x1][y1] = 1
            grid[x2][y2] = 4
            last_pos = last_pos[1]
            done = False
            return grid, last_pos, back_step, done
        else:
            index = randint(0, len(valid_steps))
            # print(f"valid: {len(valid_steps)}, chose {index}")
            last_pos = valid_steps[index]
            (x1, y1) = last_pos[0]
            (x2, y2) = last_pos[1]
            grid[x1][y1] = 1
            grid[x2][y2] = 4
            last_pos = last_pos[1]
            done = False
            return grid, last_pos, back_step, done