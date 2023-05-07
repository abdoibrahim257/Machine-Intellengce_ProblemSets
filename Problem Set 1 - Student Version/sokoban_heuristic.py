from sokoban import SokobanProblem, SokobanState
from mathutils import Direction, Point, manhattan_distance
from helpers.utils import NotImplemented

# This heuristic returns the distance between the player and the nearest crate as an estimate for the path cost
# While it is consistent, it does a bad job at estimating the actual cost thus the search will explore a lot of nodes before finding a goal
def weak_heuristic(problem: SokobanProblem, state: SokobanState):
    return min(manhattan_distance(state.player, crate) for crate in state.crates) - 1

#DONE: Import any modules and write any functions you want to use

def strong_heuristic(problem: SokobanProblem, state: SokobanState) -> float:
    #DONE: ADD YOUR CODE HERE
    #IMPORTANT: DO NOT USE "problem.get_actions" HERE.
    # Calling it here will mess up the tracking of the expanded nodes count
    # which is the number of get_actions calls during the search
    #NOTE: you can use problem.cache() to get a dictionary in which you can store information that will persist between calls of this function
    # This could be useful if you want to store the results heavy computations that can be cached and used across multiple calls of this function
    return weak_heuristic(problem,state)+ min(manhattan_distance(crate, goal) for crate in state.crates for goal in state.layout.goals) 
                                            #same as weak heuristic but with the distance to the nearest goal i.e min dist bet (me and crate + min dist bet crate and goal) 
                                                                                                                                                        #for each crate and goal 