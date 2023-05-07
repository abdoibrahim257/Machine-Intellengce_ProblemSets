from problem import HeuristicFunction, Problem, S, A, Solution
from collections import deque
from helpers.utils import NotImplemented
from queue import LifoQueue

#DONE: Import any modules you want to use
import heapq

# All search functions take a problem and a state
# If it is an informed search function, it will also receive a heuristic function
# S and A are used for generic typing where S represents the state type and A represents the action type

# All the search functions should return one of two possible type:
# 1. A list of actions which represent the path from the initial state to the final state
# 2. None if there is no solution

def BreadthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    Frontier = [] #initializing a Q for frontier
    frontSet = set() #without the use of this set will gove out time limit ----> needed for faster search synced with the frontier
    expSet = set() #explored set to check if node visited
    ac = dict() # dict to traverse on each child to get parent for back tracking
    ans = [] #empty list to store final path
    #need to check on the initial state if goal
    if problem.is_goal(initial_state): return None # y none-> this means no actions
    Frontier.append(initial_state)
    frontSet.add(initial_state) #here is the synch of the set
    while(Frontier != []):
        node = Frontier.pop(0)
        frontSet.remove(node) #here is the synch of the set
        expSet.add(node) # add node to explore set
        for action in problem.get_actions(node): #loop on available actions 
            child = problem.get_successor(node, action) #get child for each action 
            if (child not in frontSet) and (child not in expSet): # i have to check if it is not available in the frontier (here used the set for fast search) as well as the                                               
                                                                    # explored set because we are performing graph search 
                ac[child] = (node, action) #I made this dict for back tracking saving ther child as key and value => (parent, ACtion to that child)                    
                if problem.is_goal(child):
                    #start back tracking
                    i = child #getting the child to start back tracking
                    while(i in ac): #check if the child is in the dict to get the parent and the action to that parent
                        ans.append(ac[i][1])
                        i = ac[i][0]
                    return ans[::-1]
                else:        #in BFS i check if it is a goal or not before inserting in the frontier
                    Frontier.append(child)
                    frontSet.add(child)#here is the synch of the se

def DepthFirstSearch(problem: Problem[S, A], initial_state: S) -> Solution: #the dfs is the same code as the BFS
                                                                            #but we change some conditions
    Frontier = LifoQueue() #initializing a stack for frontier
    frontSet = set() #without the use of this set will gove out time limit ----> needed for faster search synced with the frontier
    expSet = set() #explored set to check if node visited
    ac = dict() # dict to traverse on each child to get parent for back tracking
    ans = [] #empty list to store final path
    #need to check on the initial state if goal
    if problem.is_goal(initial_state): return None # y none-> this means no actions
    Frontier.put(initial_state)
    frontSet.add(initial_state) #here is the synch of the set
    while(not Frontier.empty()):
        node = Frontier.get()
        frontSet.remove(node) #here is the synch of the set
        expSet.add(node) # add node to explore set
        if problem.is_goal(node): #====> here is the difference between the bfs and Dfs
            #start back tracking
            i = node
            while(i in ac):
                ans.append(ac[i][1])
                i = ac[i][0]
            return ans[::-1]
        for action in problem.get_actions(node): #loop on available actions 
            child = problem.get_successor(node, action) #get child for each action 
            if (child not in frontSet) and (child not in expSet): # i have to check if it is not available in the frontier (here used the set for fast search) as well as the                                               
                                                                # explored set because we are performing graph search 
                ac[child] = (node, action) #I made this dict for back tracking saving ther child as key and value => (parent, ACtion to that child)                    
                Frontier.put(child)
                frontSet.add(child)#here is the synch of the set


def UniformCostSearch(problem: Problem[S, A], initial_state: S) -> Solution:
    Frontier = [] #initializing a stack for frontier
    frontSet = set() #without the use of this set will gove out time limit ----> needed for faster search synced with the frontier
    expSet = set() #explored set to check if node visited
    ac = dict() # dict to traverse on each child to get parent for back tracking
    ans = [] #empty list to store final path
    #need to check on the initial state if goal
    if problem.is_goal(initial_state): return None # y none-> this means no actions
    Frontier.append((0,initial_state)) #here i add node with cost as a tuple
    frontSet.add(initial_state) #here is the synch of the set
    while(Frontier != []):
        Frontier.sort(key = lambda x : x[0])
        nodeT = Frontier.pop(0)
        frontSet.remove(nodeT[1]) #here is the synch of the set
        expSet.add(nodeT[1]) # add node to explore set
        if problem.is_goal(nodeT[1]):
            #start back tracking
            i = nodeT[1]
            while(i in ac):
                ans.append(ac[i][1])
                i = ac[i][0]
            return ans[::-1]
        for action in problem.get_actions(nodeT[1]): #loop on available actions
            child = problem.get_successor(nodeT[1], action) #get child for each action 
            if (child not in frontSet) and (child not in expSet):# i have to check if it is not available in the frontier (here used the set for fast search) as well as the                                               
                                                          # explored set because we are performing graph search 
                ac[child] = (nodeT[1], action)#I made this dict for back tracking saving ther child as key and value => (parent, ACtion to that child)           
                Frontier.append((problem.get_cost(nodeT[1],action) + nodeT[0] , child))#here is the accumlative cost part adding the cost of the path
                                                                                        #the next child  of this node if exist will add his path cost to the one added here
                                                                                        # therfore it will be accumlative 
                frontSet.add(child)#here is the synch of the set
            elif child in frontSet: #=============> in this else if i loop to replace the child if he is in the frontier with already higher cost 
                for i in range(len(Frontier)):
                    if Frontier[i][1] == child and Frontier[i][0] > (problem.get_cost(nodeT[1],action)+  nodeT[0]): #check if the current node accumlative is less than the one in frontier
                        Frontier.remove(Frontier[i])
                        ac[child] = (nodeT[1], action) #===> rinsert the child with his new parent and action
                        Frontier.append((problem.get_cost(nodeT[1],action) + nodeT[0] , child))
                        break

def AStarSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    Frontier = [] #initializing a stack for frontier
    frontSet = set() #without the use of this set will gove out time limit ----> needed for faster search synced with the frontier
    expSet = set() #explored set to check if node visited
    ac = dict() # dict to traverse on each child to get parent for back tracking
    ans = [] #empty list to store final path
    #need to check on the initial state if goal
    if problem.is_goal(initial_state): return None # y none-> this means no actions
    Frontier.append((0,initial_state)) 
    frontSet.add(initial_state) #here is the synch of the set
    while(Frontier != []):
        Frontier.sort(key = lambda x : x[0])
        nodeT = Frontier.pop(0)
        frontSet.remove(nodeT[1]) #here is the synch of the set
        expSet.add(nodeT[1]) # add node to explore set
        if problem.is_goal(nodeT[1]): #====> here is the difference between the bfs and Dfs
            #start back tracking
            i = nodeT[1]
            while(i in ac): 
                ans.append(ac[i][1]) 
                i = ac[i][0]
            return ans[::-1]
        for action in problem.get_actions(nodeT[1]): #loop on available actions
            child = problem.get_successor(nodeT[1], action) #get child for each action 
            if (child not in frontSet) and (child not in expSet): # i have to check if it is not available in the frontier (here used the set for fast search) as well as the                                               
                                                                # explored set because we are performing graph search 
                ac[child] = (nodeT[1], action)#I made this dict for back tracking saving ther child as key and value => (parent, ACtion to that child)           
                
                #here is the accumlative cost part adding the cost of the path
                #the next child  of this node if exist will add his path cost to the one added here
                # therfore it will be accumlative + the heuristic of the current node (-) its parent beecause it is not accumlative
                Frontier.append((problem.get_cost(nodeT[1],action) + nodeT[0]+ heuristic(problem,child) - heuristic(problem,nodeT[1]) , child))
                frontSet.add(child)#here is the synch of the set

            elif child in frontSet: 
                for i in range(len(Frontier)): #check if the current node accumlative cost is less than the one in frontier
                    if Frontier[i][1] == child and Frontier[i][0] > (problem.get_cost(nodeT[1],action)+  nodeT[0]+ heuristic(problem,child) - heuristic(problem,nodeT[1])):
                        Frontier.remove(Frontier[i])
                        ac[child] = (nodeT[1], action)
                        Frontier.append((problem.get_cost(nodeT[1],action) + nodeT[0]+ heuristic(problem,child) - heuristic(problem,nodeT[1]) , child))
                        break #for faster search


def BestFirstSearch(problem: Problem[S, A], initial_state: S, heuristic: HeuristicFunction) -> Solution:
    Frontier = [] #initializing a stack for frontier
    frontSet = set() #without the use of this set will gove out time limit ----> needed for faster search synced with the frontier
    expSet = set() #explored set to check if node visited
    ac = dict() # dict to traverse on each child to get parent for back tracking
    ans = [] #empty list to store final path
    #need to check on the initial state if goal
    if problem.is_goal(initial_state): return None # y none-> this means no actions
    Frontier.append((0,initial_state))
    frontSet.add(initial_state) #here is the synch of the set
    while(Frontier != []):
        Frontier.sort(key = lambda x : x[0])
        nodeT = Frontier.pop(0)
        frontSet.remove(nodeT[1]) #here is the synch of the set
        expSet.add(nodeT[1]) # add node to explore set
        if problem.is_goal(nodeT[1]): #====> here is the difference between the bfs and Dfs
            #start back tracking
            i = nodeT[1]
            while(i in ac):
                ans.append(ac[i][1])
                i = ac[i][0]
            return ans[::-1]
        for action in problem.get_actions(nodeT[1]): #loop on available actions
            child = problem.get_successor(nodeT[1], action) #get child for each action 
            if (child not in frontSet) and (child not in expSet): # i have to check if it is not available in the frontier (here used the set for fast search) as well as the                                               
                                                                # explored set because we are performing graph search 
                ac[child] = (nodeT[1], action) #I made this dict for back tracking saving ther child as key and value => (parent, ACtion to that child)                    
                     
                Frontier.append((heuristic(problem,child) , child)) #i only compare wiith the hwuristics available not the acculative so thats why i added it only
                frontSet.add(child)#here is the synch of the set
            #here no need to add the else if above as only compare with avaliable heuristics