from typing import Any, Dict, List, Optional
from CSP import Assignment, BinaryConstraint, Problem, UnaryConstraint
from helpers.utils import NotImplemented

# This function applies 1-Consistency to the problem.
# In other words, it modifies the domains to only include values that satisfy their variables' unary constraints.
# Then all unary constraints are removed from the problem (they are no longer needed).
# The function returns False if any domain becomes empty. Otherwise, it returns True.
def one_consistency(problem: Problem) -> bool:
    remaining_constraints = []
    solvable = True
    for constraint in problem.constraints:
        if not isinstance(constraint, UnaryConstraint):
            remaining_constraints.append(constraint)
            continue
        variable = constraint.variable
        new_domain = {value for value in problem.domains[variable] if constraint.condition(value)}
        if not new_domain:
            solvable = False
        problem.domains[variable] = new_domain
    problem.constraints = remaining_constraints
    return solvable

# This function returns the variable that should be picked based on the MRV heuristic.
# NOTE: We don't use the domains inside the problem, we use the ones given by the "domains" argument 
#       since they contain the current domains of unassigned variables only.
# NOTE: If multiple variables have the same priority given the MRV heuristic, 
#       we order them in the same order in which they appear in "problem.variables".
def minimum_remaining_values(problem: Problem, domains: Dict[str, set]) -> str:
    _, _, variable = min((len(domains[variable]), index, variable) for index, variable in enumerate(problem.variables) if variable in domains)
    return variable

# This function should implement forward checking
# The function is given the problem, the variable that has been assigned and its assigned value and the domains of the unassigned values
# The function should return False if it is impossible to solve the problem after the given assignment, and True otherwise.
# In general, the function should do the following:
#   - For each binary constraints that involve the assigned variable:
#       - Get the other involved variable.
#       - If the other variable has no domain (in other words, it is already assigned), skip this constraint.
#       - Update the other variable's domain to only include the values that satisfy the binary constraint with the assigned variable.
#   - If any variable's domain becomes empty, return False. Otherwise, return True.
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def forward_checking(problem: Problem, assigned_variable: str, assigned_value: Any, domains: Dict[str, set]) -> bool:
    #done: Write this function
    for constraint in problem.constraints: #loop on all the constraints in the problem
        if assigned_variable in constraint.variables: #check if the assigned variable is in the constraint
            other_variable = constraint.get_other(assigned_variable) #for each Binary constraint get the other variable and check its domain
            if domains.get(other_variable) is None: #ther other variable has no domain so it will be skipped
                continue
            domains[other_variable] = {value for value in domains[other_variable] if constraint.is_satisfied({assigned_variable:assigned_value, other_variable:value})} #update the other variable's domain
            if not domains.get(other_variable): #if any variable's domain becomes empty, return False
                return False
    return True #Otherwise, return True.


# This function should return the domain of the given variable order based on the "least restraining value" heuristic.
# IMPORTANT: This function should not modify any of the given arguments.
# Generally, this function is very similar to the forward checking function, but it differs as follows:
#   - You are not given a value for the given variable, since you should do the process for every value in the variable's
#     domain to see how much it will restrain the neigbors domain
#   - Here, you do not modify the given domains. But you can create and modify a copy.
# IMPORTANT: If multiple values have the same priority given the "least restraining value" heuristic, 
#            order them in ascending order (from the lowest to the highest value).
# IMPORTANT: Don't use the domains inside the problem, use and modify the ones given by the "domains" argument 
#            since they contain the current domains of unassigned variables only.
def least_restraining_values(problem: Problem, variable_to_assign: str, domains: Dict[str, set]) -> List[Any]:
    #DONE: Write this function
    temp_domains = domains.copy() # create a copy of the domains to modify thena and detect number of changes in the domains
    to_sort = []
    for value in temp_domains[variable_to_assign]: #loop on the values of the variable to assign
        counter = 0 #counter to detect number of changes in the domains
        for constraint in problem.constraints: #loop on the values of the variable to assign
            if variable_to_assign in constraint.variables: #check if the assigned variable is in the constraint
                other_variable = constraint.get_other(variable_to_assign) #for each Binary constraint get the other variable and check its domain
                if temp_domains.get(other_variable) is None: #ther other variable has no domain so it will be skipped
                    continue
                for other_value in temp_domains[other_variable]:
                    if not constraint.is_satisfied({variable_to_assign:value, other_variable:other_value}):
                        counter+=1 #increase the counter if the constraint is not satisfied
        to_sort.append((counter, value)) #append the value and the counter to the list to sort
    to_sort.sort(key=lambda s: (s[0],s[1])) #sort the list
    return [value for _, value in to_sort] #return the sorted list


# This function should solve CSP problems using backtracking search with forward checking.
# The variable ordering should be decided by the MRV heuristic.
# The value ordering should be decided by the "least restraining value" heurisitc.
# Unary constraints should be handled using 1-Consistency before starting the backtracking search.
# This function should return the first solution it finds (a complete assignment that satisfies the problem constraints).
# If no solution was found, it should return None.
# IMPORTANT: To get the correct result for the explored nodes, you should check if the assignment is complete only once using "problem.is_complete"
#            for every assignment including the initial empty assignment, EXCEPT for the assignments pruned by the forward checking.
#            Also, if 1-Consistency deems the whole problem unsolvable, you shouldn't call "problem.is_complete" at all.
def solve(problem: Problem) -> Optional[Assignment]:
    #DONE: Write this function
    asssignment : Assignment = {}
    if not one_consistency(problem): #check if the problem is not 1-consistent
        return None
    return backtracking_search(problem, asssignment, problem.domains) #return the result of the backtracking search

def backtracking_search(problem: Problem, assignment:Assignment, domains: Dict[str, set]) -> Optional[Assignment]:
     
    if problem.is_complete(assignment): #check if the assignment is complete
        return assignment

    start_variable = minimum_remaining_values(problem, domains) #get the variable with the minimum remaining values
    strtVar_values = least_restraining_values(problem, start_variable, domains) #get the values of the variable sorted according to the least restraining values heuristic
    for value in strtVar_values: #loop on the values of the variable
        assignment[start_variable] = value #assign the value to the variable since one consistency is done to start applying forward checking
        temp_domain =  {}
        for set in domains: #lop to copy domian and remove the start variable from it to not change in the original domain for the next iteration and to apply forward checking on the remaingin variables
            if set != start_variable:
                temp_domain[set] = domains[set].copy()
        if forward_checking(problem, start_variable, value, temp_domain): #apply forward checking on the problem
            result = backtracking_search(problem, assignment, temp_domain) #call the backtracking search function recursively
            if result is not None: #check if the result is not 
                return result
    return None
