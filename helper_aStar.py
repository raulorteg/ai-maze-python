# -*- coding: utf-8 -*-
"""
Created on Sun Sep 13 13:52:56 2020
@author: Raul Ortega Ochoa
"""
import csv
import numpy as np

class Node: # define a Node class
    def __init__(self, parent, cost, position):
        self.parent = parent
        self.cost = cost
        self.position = position

# =========================================

def remove_node_frontier(node, frontier):
    """
    Parameters
    ----------
    node : node object
        node to be removed from frontier.
    frontier : list
        list of nodes in the frontier.
    Returns
    -------
    new_frontier : list
        frontier updated without the node
    """
    pos = node.position
    new_frontier = []
    for item in frontier:
        if item.position != pos:
            new_frontier.append(item)
    return new_frontier

# =========================================

def compute_node_cost(pos, goal):
    """
    Parameters
    ----------
    pos : tuple of 2 ints
        position of node whos cost want to compute.
    goal : tuple of 2 ints
        position of goal.
    Returns
    -------
    cost : float
        euclidean distance pos-goal
    """
    x, y = pos
    x_goal, y_goal = goal
    cost = np.sqrt((x_goal-x)**2 + (y_goal-y)**2)
    return cost

# ========================================

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

def compute_successors(current_node, grid, seen):
    """
    Parameters
    ----------
    current_node : node object
        node whos successsors want to compute.
    grid : list of lists
        the maze grid system.
    seen : list of nodes
         list of nodes already seen
    Returns
    -------
    successors : list of node objects
        list of nodes succesors
    """
    movements = [(1,0), (-1,0), (0,1), (0,-1)]
    x_0, y_0 = current_node.position
    grid_dim = (len(grid)-1, len(grid[0])-1)
            
    successors = []
    for movement in movements:
        dx, dy = (movement[0], movement[1])
        next_pos = (x_0+dx, y_0+dy)
        cond1 = is_in_map(next_pos, grid_dim) # if its on the map
        if cond1:
            cond2 = grid[next_pos[0], next_pos[1]] != 0 # if not wall
            cond3 = next_pos not in [item.position for item in seen] # dont go to any already seen
            if bool(cond2*cond3):
                cost = compute_node_cost(next_pos, grid_dim)
                new_node = Node(current_node, cost, next_pos)
                successors.append(new_node)
    return successors

# =============================
def pick_node_from_list(node_list):
    """
    Parameters
    ----------
    node_list : list of nodes
        list of nodes.
    Returns
    -------
    current_node : node object
        node with least cost among those
        in the list.
    """
    if len(node_list) == 1:
        current_node = node_list[0]
        return current_node
    
    current_node = Node(None, np.inf, (0,0)) # initialize current node
    for node in node_list:
        if node.cost < current_node.cost: # pick up the node with least cost
            current_node = node
    return current_node

# =============================
# grid, frontier, seen, current_node = generate_step(grid, frontier, seen, current_node)
def generate_step(grid, frontier, seen, current_node):
    """
    Parameters
    ----------
    grid : list of list of ints
        grid system of the maze.
    frontier : list of nodes
        list of nodes in the frontier.
    seen : list of nodes
        list of nodes already seen.
    current_node : node object
        Current node the ai is in.
    Returns
    -------
    grid : list of list of ints
        updated grid system of the maze
    frontier : list of nodes
        updated list of nodes in frontier
    seen : list of nodes
        updated list of nodes already seen
    current_node : node object
        updated node where ai is in
    """
    # add parent to seen list
    seen.append(current_node)
    
    # remove parent from frontier
    frontier = remove_node_frontier(current_node, frontier)
    
    # given the node compute the successors
    successors = compute_successors(current_node, grid, seen)
    
    # add successors to the frontier
    for son in successors:
        frontier.append(son)

    # pick one of the successors
    current_node = pick_node_from_list(successors)
    
    # paint the grid with the new node position
    x, y = current_node.position
    grid[x, y] = 4 # paint blue
    
    return grid, frontier, seen, current_node