from typing import Tuple
import re
from CSP import Assignment, Problem, UnaryConstraint, BinaryConstraint

#TODO (Optional): Import any builtin library or define any helper function you want to use

# This is a class to define for cryptarithmetic puzzles as CSPs
class CryptArithmeticProblem(Problem):
    LHS: Tuple[str, str]
    RHS: str

    # Convert an assignment into a string (so that is can be printed).
    def format_assignment(self, assignment: Assignment) -> str:
        LHS0, LHS1 = self.LHS
        RHS = self.RHS
        letters = set(LHS0 + LHS1 + RHS)
        formula = f"{LHS0} + {LHS1} = {RHS}"
        postfix = []
        valid_values = list(range(10))
        for letter in letters:
            value = assignment.get(letter)
            if value is None: continue
            if value not in valid_values:
                postfix.append(f"{letter}={value}")
            else:
                formula = formula.replace(letter, str(value))
        if postfix:
            formula = formula + " (" + ", ".join(postfix) +  ")" 
        return formula

    @staticmethod
    def from_text(text: str) -> 'CryptArithmeticProblem':
        # Given a text in the format "LHS0 + LHS1 = RHS", the following regex
        # matches and extracts LHS0, LHS1 & RHS
        # For example, it would parse "SEND + MORE = MONEY" and extract the
        # terms such that LHS0 = "SEND", LHS1 = "MORE" and RHS = "MONEY"
        pattern = r"\s*([a-zA-Z]+)\s*\+\s*([a-zA-Z]+)\s*=\s*([a-zA-Z]+)\s*"
        match = re.match(pattern, text)
        if not match: raise Exception("Failed to parse:" + text)
        LHS0, LHS1, RHS = [match.group(i+1).upper() for i in range(3)]

        problem = CryptArithmeticProblem()
        problem.LHS = (LHS0, LHS1)
        problem.RHS = RHS

        #TODO Edit and complete the rest of this function
        # problem.variables:    should contain a list of variables where each variable is string (the variable name)
        # problem.domains:      should be dictionary that maps each variable (str) to its domain (set of values)
        #                       For the letters, the domain can only contain integers in the range [0,9].
        # problem.constaints:   should contain a list of constraint (either unary or binary constraints).

        def permutaion(c1, c2): #returns a set of tuples of all the possible permutations of the two variables
            retSet = set()
            for i in problem.domains[c1]:
                for j in problem.domains[c2]:
                    retSet.add((i,j))
            return retSet
        
        def permutaion2(c1, c2, c3): #returns a set of tuples of all the possible permutations of the two variables
            return {(i, j, k) for i in problem.domains[c1] for j in problem.domains[c2] for k in problem.domains[c3]} #tried to make it more efficient 030 but couldn't :(

        problem.variables = []
        problem.domains = {}
        problem.constraints = []

        #assigning the values to the variables without the carry

        problem.domains[LHS0[0]] = set(range(1, 10)) #the first letter of the LHS0 cannot be 0
        problem.variables.append(LHS0[0]) #adding the first letter of the LHS0 to the variables list

        problem.domains[LHS1[0]] = set(range(1, 10)) #the first letter of the LHS1 cannot be 0
        if LHS1[0] not in problem.variables: #adding the first letter of the LHS1 to the variables list if it is not already there
            problem.variables.append(LHS1[0])

        carryNum = max(len(LHS0), len(LHS1)) #the number of carry variables needed is the max of the lengths of the LHS0 and LHS1

        if(len(RHS) > max(len(LHS0), len(LHS1))): 
            problem.domains[RHS[0]] = set(range(1,2)) #make the set of RHS[0]  = 1 if the length of RHS is greater than the max of the lengths of the LHS0 and LHS1
        else:
            problem.domains[RHS[0]] = set(range(1, 10)) #else the set of RHS[0] = 1 to 9 the normal case

        if RHS[0] not in problem.variables: #adding the first letter of the RHS to the variables list if it is not already there
            problem.variables.append(RHS[0])

        for letter in range(1,len(LHS0)): #adding the rest of the letters of the LHS0 to the variables list and assigning their domains
            if LHS0[letter] not in problem.variables: #adding the letter to the variables list if it is not already there
                problem.variables.append(LHS0[letter])
            if LHS0[letter] not in problem.domains:  #assigning the domain of the letter if it is not already assigned
                problem.domains[LHS0[letter]] = set(range(10))

        for letter in range(1,len(LHS1)): #adding the rest of the letters of the LHS1 to the variables list and assigning their domains
            if LHS1[letter] not in problem.variables:
                problem.variables.append(LHS1[letter])
            if LHS1[letter] not in problem.domains:
                problem.domains[LHS1[letter]] = set(range(10))
 
        for letter in range(1,len(RHS)): #adding the rest of the letters of the RHS to the variables list and assigning their domains
            if RHS[letter] not in problem.variables: #adding the letter to the variables list if it is not already there
                problem.variables.append(RHS[letter])
            if RHS[letter] not in problem.domains: #assigning the domain of the letter if it is not already assigned
                problem.domains[RHS[letter]] = set(range(10))

        #############################################################all_diff
        for i in range(len(problem.variables)): 
            for j in range(i+1, len(problem.variables)):
                problem.constraints.append(BinaryConstraint((problem.variables[i], problem.variables[j]), lambda x, y: x != y))
        ####################################################################

        ########################################## assigning the values carry
        for c in range(carryNum): #adding the carry variables to the variables list and assigning their domains
            if "C" + str(c) not in problem.variables:
                problem.variables.append("C" + str(c))
                problem.domains["C" + str(c)] = set(range(2))

        if(len(RHS) > max(len(LHS0), len(LHS1))): #special case if the length of the RHS is greater than the max of the lengths of the LHS0 and LHS1
            problem.domains["C" + str(carryNum-1)] = set(range(1,2)) #make the set of the last carry variable = 1
        #assigning the constraints
        

        #special cases i have is for the first and last letter of the LHS and RHs
        
        ###################################################################first letter of LHS0 and LHS1
        k = 0 #counter for the carry variables, 0 indexed 
        A = LHS0[len(LHS0)-1]+LHS1[len(LHS1)-1] #a string combining the RHS equation
        c = "C" + str(k)
        B = RHS[len(RHS)-1] + c #a string combining the RHS equation
        problem.variables.append(A) #adding the variables to the variables list
        problem.domains[A] = permutaion(A[0],A[1]) #assigning the domain of the variables using the permutation function
        problem.variables.append(B) #adding the variable B to the variables list
        problem.domains[B] = permutaion(B[0],c) #assigning the domain of the variables using the permutation function

        #will be using lambda equations to assign the constraints equations

        #LHS Equation contraints
        #constraint bonding the first letter in A with the first letter in LHS0
        problem.constraints.append(BinaryConstraint((A[0], A), (lambda x, y: x == y[0]))) #A[0] = LHS0[len(LHS0)-1]

        #constraint bonding the second letter in A with the first letter in LHS1
        problem.constraints.append(BinaryConstraint((A[1], A), (lambda x, y: x == y[1]))) #A[1] = LHS1[len(LHS1)-1]

        #RHS Equation

        #constraint bonding the first letter in B with the first letter in RHS
        problem.constraints.append(BinaryConstraint((B[0], B), (lambda x, y: x == y[0]))) #B[0] = RHS[len(RHS)-1]
        #constraint bonding the second letter in B with the first letter in C0
        problem.constraints.append(BinaryConstraint((B[1:], B), (lambda x, y: x == y[1]))) #B[1:] = C0

        #here i will be making sure that the RHS = LHS equation
        problem.constraints.append(BinaryConstraint((A, B), (lambda x, y: x[0] + x[1] == y[0] + 10*y[1]))) #LHS0[len(LHS0)-1] + LHS1[len(LHS1)-1] = RHS[len(RHS)-1] + C0


        #####################################################################################now compute in betweeen
        equalLenOfLHS = min(len(LHS0), len(LHS1)) #the length of the smaller LHS

        whichSmaller = 1 if len(LHS1) <= len(LHS0) else 0 #which LHS is smaller 

        diff = abs(len(LHS0) - len(LHS1)) #the difference in length between the two LHS

        diffRHS = abs(len(RHS) - equalLenOfLHS) #the difference in length between the RHS and the smaller LHS

        for i in range(equalLenOfLHS-2,-1,-1): #looping through the smaller LHS from the second last letter to the first letter of the smaller LHS
            if whichSmaller:
                #index of LHS1 is the same as i 
                #in index of LHS0 the i is the current i we traverse plus the difference between them
                A = LHS0[i+diff]+LHS1[i] + "C" + str(k) #a string combining the LHS equation 
            else: ##############################the difference here is in indexing which is why i have the if statement
                #index of LHS0 is the same as i
                #in index of LHS1 the i is the current i we traverse plus the difference between them
                A = LHS0[i]+LHS1[i+diff] + "C" + str(k) #a string combining the LHS equation LHS0[i]+LHS1[i+diff]+CK

            problem.variables.append(A) #adding the variable A to the variables list
            problem.domains[A] = permutaion2(A[0],A[1],A[2:]) #assigning the domain of the variables using the permutation function wit tree inputs since in the RHS i have Carry with me 

            # same set of constraints as the first letter of LHS0 and LHS1 but one additional becaue here we have the carry variable in LHS
            problem.constraints.append(BinaryConstraint((A[0], A), lambda x, y: x == y[0])) #A[0] = LHS0[i+diff]
            problem.constraints.append(BinaryConstraint((A[1], A), lambda x, y: x == y[1])) #A[1] = LHS1[i]
            problem.constraints.append(BinaryConstraint((A[2:], A), lambda x, y: x == y[2])) #A[2:] = CK  #the new one

            k+=1 #incrementing the carry variable counter for the carry in the output 
            B = RHS[i+diffRHS] + "C" + str(k) #a string combining the RHS equation B = RHS[i+diffRHS] + CK
            problem.variables.append(B) #adding the variable B to the variables list
            problem.domains[B] = permutaion(B[0],B[1:]) #assigning the domain of the variables using the permutation function
            problem.constraints.append(BinaryConstraint((B[0], B), lambda x, y: x == y[0])) #B[0] = RHS[i+diffRHS]
            problem.constraints.append(BinaryConstraint((B[1:], B), lambda x, y: x == y[1])) #B[1:] = CK
            problem.constraints.append(BinaryConstraint((A, B), lambda x, y: x[0] + x[1] + x[2] == y[0] + 10*y[1])) #LHS0[i+diff]+LHS1[i] + CK = RHS[i+diffRHS] + CK+1

        ###############################################################now compute the rest of the LHS that doent have a corresponding RHS
        maxL = LHS0 if len(LHS0) > len(LHS1) else LHS1 #the longer LHS
        d = abs(len(maxL) - len(RHS)) #the difference in length between the longer LHS and the RHS for traversing on RHS
        for i in range(diff-1,-1,-1): #looping through the longer LHS from the second last letter to the first letter
            A = maxL[i] + "C" + str(k) 
            problem.variables.append(A) #adding the variable A to the variables list
            problem.domains[A] = permutaion(A[0],A[1:]) #assigning the domain of the variables using the permutation function
            problem.constraints.append(BinaryConstraint((A[0], A), lambda x, y: x == y[0])) #A[0] = maxL[i+diff]
            problem.constraints.append(BinaryConstraint((A[1:], A), lambda x, y: x == y[1])) #A[1:] = CK
            k+=1
            B = RHS[i+ d] + "C" + str(k) #a string combining the RHS equation B = RHS[i+ d] + CK where d here is the difference in length between the longer LHS and the RHS for traversing on RHS
            problem.variables.append(B)
            problem.domains[B] = permutaion(B[0],B[1:]) #assigning the domain of the variables using the permutation function
            problem.constraints.append(BinaryConstraint((B[0], B), lambda x, y: x == y[0])) #B[0] = RHS[i+ d]
            problem.constraints.append(BinaryConstraint((B[1:], B), lambda x, y: x == y[1])) #B[1:] = CK
            problem.constraints.append(BinaryConstraint((A, B), lambda x, y: x[0] + x[1] == y[0] + 10*y[1])) #maxL[i+diff] + CK = RHS[i+ d] + CK+1 where the ck+1 here is already 
                                                                                #assinged to the alst variable in the RHS if it's length is greater than the longer both LHS
                                                                                #else i dont need to care about the CK+1 if RHS is equal to the longer LHS

        return problem

        
    @staticmethod
    def from_file(path: str) -> "CryptArithmeticProblem":
        with open(path, 'r') as f:
            return CryptArithmeticProblem.from_text(f.read())
        


 #assigning the constraints
        # for i in min(LHS0, LHS1, RHS): i -= 1
        #10*c0 + LHS0[i] + LHS1[i] = RHS[i] + c1
        
        # equalLenOfLHS = min(len(LHS0), len(LHS1)) - 1

        # whichLHS = 1 if len(LHS1) > len(LHS0) else 0
        # k=0
        # for i in range(equalLenOfLHS,-1,-1): #computing only the equal length of the LHS and RHS
        #     #LHS0[i] + LHS1[i] + c+k = RHS[i] + c+k+1
        #     lhsContraint = BinaryConstraint((LHS0[i], LHS1[i]), lambda x, y: x + y == LHS0[i] + LHS1[i])
        #     problem.constraints.append(lhsContraint)
        #     if i != equalLenOfLHS:
        #         ck = "C" + str(k)
        #         lhsCarryContraint = BinaryConstraint((lhsContraint, "C" + str(k)), lambda x, y: x + y == lhsContraint + ck)
        #         problem.constraints.append(lhsCarryContraint)
        #         k+=1
        #     ckPlus = "C" + str(k)
        #     rhsContraint = BinaryConstraint((RHS[i], ckPlus), lambda x, y: x + y == RHS[i] + ckPlus)
        #     problem.constraints.append(rhsContraint)
        #     equationConstraint = BinaryConstraint((lhsCarryContraint, rhsContraint), lambda x, y: x == y)
        #     problem.constraints.append(equationConstraint)