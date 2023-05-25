from typing import Dict, Optional
from agents import Agent
from environment import Environment
from mdp import MarkovDecisionProcess, S, A
import json
from helpers.utils import NotImplemented

# This is a class for a generic Value Iteration agent
class ValueIterationAgent(Agent[S, A]):
    mdp: MarkovDecisionProcess[S, A] # The MDP used by this agent for training 
    utilities: Dict[S, float] # The computed utilities
                                # The key is the string representation of the state and the value is the utility
    discount_factor: float # The discount factor (gamma)

    def __init__(self, mdp: MarkovDecisionProcess[S, A], discount_factor: float = 0.99) -> None:
        super().__init__()
        self.mdp = mdp
        self.utilities = {state:0 for state in self.mdp.get_states()} # We initialize all the utilities to be 0
        self.discount_factor = discount_factor
    
    # Given a state, compute its utility using the bellman equation
    # if the state is terminal, return 0
    def compute_bellman(self, state: S) -> float:
        #DONE: Complete this function
        if self.mdp.is_terminal(state): #if the state is terminal, retun 0
            return 0
        maxUtil = float('-inf') # initialize the max utility to -inf
        for action in self.mdp.get_actions(state): # for each action in the state
            successors = self.mdp.get_successor(state, action) # get the successors of the state
            util = 0 # summer of all the utilities of the successor
            for successor, prob in successors.items(): # for each successor run the bellman equation
                util += prob * (self.mdp.get_reward(state, action, successor) + self.discount_factor * self.utilities[successor]) #bellman equation that computes the utility of the successor
            maxUtil = max(maxUtil, util) # get the max utility of each action
        return maxUtil

    # Applies a single utility update
    # then returns True if the utilities has converged (the maximum utility change is less or equal the tolerance)
    # and False otherwise
    def update(self, tolerance: float = 0) -> bool:
        #DONE: Complete this function
        newUtils = {}
        tempList = []
        for state in self.mdp.get_states(): #for each state in the mdp i will compute the bellman equation and store it in a temp dictionary havinge 
            newUtils[state] = self.compute_bellman(state) #compute the bellman equation for each state in a temp dectionary
            tempList.append(abs(newUtils[state] - self.utilities[state])) #list the difference between the new and old utilities in a temp list to get the max change
        #created a new dictionary with new utilities for each state
        maxChange = max(tempList) #get the max change
        self.utilities = newUtils #update the utilities with the new utilities
        return (maxChange <= tolerance) #return true if the max change is less than or equal to the tolerance else return false
        

    # This function applies value iteration starting from the current utilities stored in the agent and stores the new utilities in the agent
    # NOTE: this function does incremental update and does not clear the utilities to 0 before running
    # In other words, calling train(M) followed by train(N) is equivalent to just calling train(N+M)
    def train(self, iterations: Optional[int] = None, tolerance: float = 0) -> int:
        #DONE: Complete this function to apply value iteration for the given number of iterations

        # keep counting the number of iterations until convergence in bellman 
        itr = 0 #set the iteration to 0
        while iterations is None or itr < iterations: #while the iteration is less than the given iteration or the iteration is none
            itr += 1 #increment the iteration
            if self.update(tolerance): #if the update function returns true => converged
                break #break out of the loop and return the iteration number
        return itr #return the iteration
    
    # Given an environment and a state, return the best action as guided by the learned utilities and the MDP
    # If the state is terminal, return None
    def act(self, env: Environment[S, A], state: S) -> A:
        #DONE: Complete this function
        #this function is similar to the compute_bellman function but instead of returning the max utility, it returns the best action
        if self.mdp.is_terminal(state): #if the state is terminal,
            return None
    
        maxUtil = float('-inf') #initialize the max utility to -inf
        bestAction = None #initialize the best action to None for now
        for action in env.actions(): #for each action in the state environment actions 
            successors = self.mdp.get_successor(state, action) #get the successors of the state 
            util = 0 #summer of all the utilities of the successor
            for successor, prob in successors.items(): #for each successor run the bellman equation
                util += prob * (self.mdp.get_reward(state, action, successor) + self.discount_factor * self.utilities[successor])
            if util > maxUtil: #maximise the utility and get the best action
                maxUtil = util
                bestAction = action #get the best action with the max utility
        return bestAction #return the best action
    
    # Save the utilities to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            utilities = {self.mdp.format_state(state): value for state, value in self.utilities.items()}
            json.dump(utilities, f, indent=2, sort_keys=True)
    
    # loads the utilities from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            utilities = json.load(f)
            self.utilities = {self.mdp.parse_state(state): value for state, value in utilities.items()}
