from typing import Tuple
from game import HeuristicFunction, Game, S, A
from helpers.utils import NotImplemented

#DONE: Import any modules you want to use

# All search functions take a problem, a state, a heuristic function and the maximum search depth.
# If the maximum search depth is -1, then there should be no depth cutoff (The expansion should not stop before reaching a terminal state) 

# All the search functions should return the expected tree value and the best action to take based on the search results

# This is a simple search function that looks 1-step ahead and returns the action that lead to highest heuristic value.
# This algorithm is bad if the heuristic function is weak. That is why we use minimax search to look ahead for many steps.
def greedy(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    agent = game.get_turn(state)
    
    terminal, values = game.is_terminal(state)
    if terminal: return values[agent], None

    actions_states = [(action, game.get_successor(state, action)) for action in game.get_actions(state)]
    value, _, action = max((heuristic(game, state, agent), -index, action) for index, (action , state) in enumerate(actions_states))
    return value, action

# Apply Minimax search and return the game tree value and the best action
# Hint: There may be more than one player, and in all the testcases, it is guaranteed that 
# game.get_turn(state) will return 0 (which means it is the turn of the player). All the other players
# (turn > 0) will be enemies. So for any state "s", if the game.get_turn(s) == 0, it should a max node,
# and if it is > 0, it should be a min node. Also remember that game.is_terminal(s), returns the values
# for all the agents. So to get the value for the player (which acts at the max nodes), you need to
# get values[0].
def minimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #DONE: Complete this function
    terminal, values = game.is_terminal(state) #get the termianl state and the values of all agents
    if terminal: #check if terminal state
        return values[0], None #if true i will return values[0] and no action
    
    if max_depth==0: #leaf node
        return heuristic(game, state, 0), None #if max depth is 0 i will return the heuristic value that i will maximise or minimize upon it and no action

    if game.get_turn(state)==0: #max node
        actions = game.get_actions(state) #get actions available for the max state
        max_value = float('-inf') # and will try to maximise the value retunred from the min nodes
        for action in actions: #here i will loop on all the actions i have and maximise on the retuned min values
            successor = game.get_successor(state, action)
            value, _ = minimax(game, successor, heuristic, max_depth-1)  #get the min value returned from the min nodes
            if value > max_value: #maximise on the min values
                max_value = value
                nextAction = action
        return max_value, nextAction
    else: #min nodes
        actions = game.get_actions(state) #get actions available for the min states
        min_value = float('inf') 
        for action in actions: #here i will loop on all the actions i have and minimise on the retuned leaf nodes
            successor = game.get_successor(state, action)
            value, _ = minimax(game, successor, heuristic, max_depth-1)  #get the leaf value returned from the leaf nodes
            if value < min_value: #minimise on the leaf values
                min_value = value
                nextAction = action
        return min_value, nextAction

# Apply Alpha Beta pruning and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = float('-inf'), Beta: float = float('inf')) -> Tuple[float, A]:
    #DONE: Complete this function
    terminal, values = game.is_terminal(state) #get the termianl state and the values of all agents
    if terminal: #check if terminal state
        return values[0], None #if true i will return values[0] and no action
    
    if max_depth==0: #leaf node
        return heuristic(game, state, 0), None #if max depth is 0 i will return the heuristic value that i will maximise or minimize upon it and no action

    if game.get_turn(state)==0: #max node
        actions = game.get_actions(state) #get actions available for the max state
        max_value = float('-inf') # and will try to maximise the value retunred from the min nodes
        for action in actions: #here i will loop on all the actions i have and maximise on the retuned min values
            successor = game.get_successor(state, action)
            value, _ = alphabeta(game, successor, heuristic, max_depth-1, alpha, Beta)  #get the min value returned from the min nodes
            if value > max_value: #maximise on the min values
                max_value = value
                nextAction = action
            if max_value >= Beta: #pruning part
                return (max_value, nextAction) #if the max value is greater than or equal to Beta i will return the max value and the action
            alpha = max(alpha, max_value) #update alpha with max of alpha and max value
        return (max_value, nextAction) #if the max value is less than Beta i will return the max value and the action
    else: #min nodes
        actions = game.get_actions(state) #get actions available for the max state
        min_value = float('inf') # and will try to maximise the value retunred from the min nodes
        for action in actions: #here i will loop on all the actions i have and maximise on the retuned min values
            successor = game.get_successor(state, action)
            value, _ = alphabeta(game, successor, heuristic, max_depth-1, alpha, Beta)  #get the min value returned from the min nodes
            if value < min_value: #minimise on the leaf values
                min_value = value
                nextAction = action
            if min_value <= alpha: #pruning part
                return (min_value, nextAction) #if the min value is less than or equal to alpha i will return the min value and the action
            Beta = min(Beta, min_value) #update Beta with min of Beta and min value
        return (min_value, nextAction)
    
# Apply Alpha Beta pruning with move ordering and return the tree value and the best action
# Hint: Read the hint for minimax.
def alphabeta_with_move_ordering(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1, alpha: float = float('-inf'), Beta: float = float('inf') ) -> Tuple[float, A]:
    #DONE: Complete this function
    terminal, values = game.is_terminal(state) #get the termianl state and the values of all agents
    if terminal: #check if terminal state
        return values[0], None #if true i will return values[0] and no action
    
    if max_depth==0: #leaf node
        return heuristic(game, state, 0), None #if max depth is 0 i will return the heuristic value that i will maximise or minimize upon it and no action

    if game.get_turn(state)==0: #max node
        actions = game.get_actions(state) #get actions available for the max state
        max_value = float('-inf') # and will try to maximise the value retunred from the min nodes
        
        actionList_sorted = []
        for action in actions: #here i will loop on the actions and get the heuristic value for each action and append it to the list 
            successor = game.get_successor(state, action)
            temp = heuristic(game, successor, 0)
            actionList_sorted.append((temp, action)) #save action and heuristic value in a list of tuples
        actionList_sorted.sort(key=lambda x: x[0],reverse=True) #sort the list in descending order

        for action in actionList_sorted:# loop on the sorted list and maximise on the retuned min values with pruning part applied exactly the same as the previous function
            successor = game.get_successor(state, action[1])
            value, _ = alphabeta_with_move_ordering(game, successor, heuristic, max_depth-1, alpha, Beta)  #get the min value returned from the min nodes
            if value > max_value: #maximise on the min values
                max_value = value
                nextAction = action[1]
            if max_value >= Beta: #pruning part
                return (max_value, nextAction) #if the max value is greater than or equal to Beta i will return the max value and the action
            alpha = max(alpha, max_value) #update alpha with max of alpha and max value
        return (max_value, nextAction)
    else: #min nodes
        actions = game.get_actions(state) #get actions available for the max state
        min_value = float('inf') # and will try to maximise the value retunred from the min nodes
        
        actionList_sorted = []
        for action in actions: #here i will loop on the actions and get the heuristic value for each action and append it to the list same as max node
            successor = game.get_successor(state, action)
            temp = heuristic(game, successor, game.get_turn(state)) # but here the heuristic will take the turn of the current agent in its calculation
            actionList_sorted.append((temp, action))
        actionList_sorted.sort(key=lambda x: x[0], reverse=True) #sort the list in descending order
        
        for action in actionList_sorted: #here i will loop on all the actions i have and maximise on the retuned min values
            successor = game.get_successor(state, action[1])
            value, _ = alphabeta_with_move_ordering(game, successor, heuristic, max_depth-1, alpha, Beta)  #get the min value returned from the min nodes
            if value < min_value: #minimise on the leaf values
                min_value = value
                nextAction = action[0]
            if min_value <= alpha: #pruning part
                return (min_value, nextAction) #if the min value is less than or equal to alpha i will return the min value and the action
            Beta = min(Beta, min_value) #update Beta with min of Beta and min value
        return (min_value, nextAction)  

# Apply Expectimax search and return the tree value and the best action
# Hint: Read the hint for minimax, but note that the monsters (turn > 0) do not act as min nodes anymore,
# they now act as chance nodes (they act randomly).
def expectimax(game: Game[S, A], state: S, heuristic: HeuristicFunction, max_depth: int = -1) -> Tuple[float, A]:
    #DONE: Complete this function
    terminal, values = game.is_terminal(state) #get the termianl state and the values of all agents
    if terminal: #check if terminal state
        return values[0], None #if true i will return values[0] and no action
    
    if max_depth==0: #leaf node
        return heuristic(game, state, 0), None #if max depth is 0 i will return the heuristic value that i will maximise or minimize upon it and no action

    if game.get_turn(state)==0: #max node
        actions = game.get_actions(state) #get actions available for the max state
        max_value = float('-inf') # and will try to maximise the value retunred from the min nodes
        for action in actions: #here i will loop on all the actions i have and maximise on the retuned min values
            successor = game.get_successor(state, action)
            value, _ = expectimax(game, successor, heuristic, max_depth-1)  #get the min value returned from the min nodes
            if value > max_value: #maximise on the min values
                max_value = value
                nextAction = action
        return max_value, nextAction
    else: #expecti nodes
        actions = game.get_actions(state) #get actions available for the max state
        chance = 1/len(actions) #chance of each action
        expecti = 0
        for action in actions:
            successor = game.get_successor(state, action)
            expecti +=  expectimax(game, successor, heuristic, max_depth-1)[0] #get the value returned from the leaf nodes and sum them
        expecti *= chance #multiply the sum with the chance of each action
        return expecti, None #return the expecti value and no action