# ai-maze-python
<img src = "pathfinder_result.png"/>

ai_pathfinder.py: 
  Solves a given maze using a* algorithm and uses pygame to visualize the solving
  process. At the end prints the grid with the solution found and all the cells explored.

helper_ai_pathfinder.py: 
  helper functions used in ai_pathfinder.py
  
dumb_pathfinder.py:
  Solves a given maze using Depth-first search (DFS) algorithm and uses Pygame to visualize
  the solving proccess. Not really eficient and many times it explores all the maze before finding the solution.

helper_pathfinder.py:
  helper functions used in dumb_pathfinder.py

maze_generator.py:
  Generates a maze using Depth-first search (DFS) algorithm and uses Pygame to
  visualize the proccess of generating the maze.

helper_maze_generator.py:
  helper functions used in maze_generator.py
  
mazes folder:
  contains 20 mazes in csv format generated using maze_generator.py

mazes_solutions:
  contains the solutions to the 20 mazes in mazes folder. The solutions are the ones
  given by ai_pathfinder.py, which uses the a* algorithm.
