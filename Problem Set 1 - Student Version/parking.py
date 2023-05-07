from typing import Any, Dict, Set, Tuple, List
from problem import Problem
from mathutils import Direction, Point
from helpers.utils import NotImplemented

#DONE: (Optional) Instead of Any, you can define a type for the parking state
ParkingState = Tuple[Point] # A tuple of points where state[i] is the position of car 'i'. and I decided to make it a tuple to be similar to cars

# An action of the parking problem is a tuple containing an index 'i' and a direction 'd' where car 'i' should move in the direction 'd'.
ParkingAction = Tuple[int, Direction]

# This is the implementation of the parking problem
class ParkingProblem(Problem[ParkingState, ParkingAction]):
    passages: Set[Point]    # A set of points which indicate where a car can be (in other words, every position except walls).
    cars: Tuple[Point]      # A tuple of points where state[i] is the position of car 'i'. 
    slots: Dict[Point, int] # A dictionary which indicate the index of the parking slot (if it is 'i' then it is the lot of car 'i') for every position.
                            # if a position does not contain a parking slot, it will not be in this dictionary.
    width: int              # The width of the parking lot.
    height: int             # The height of the parking lot.

    # This function should return the initial state
    def get_initial_state(self) -> ParkingState:
        return self.cars
    
    # This function should return True if the given state is a goal. Otherwise, it should return False.
    def is_goal(self, state: ParkingState) -> bool:
        #need to check if each car is on its slot
        for s in range(len(state)): #loop as index in order to get index of car for checking if the slot that the car at is correct
            if self.slots.get(state[s]) != s: #checking if the slot that the car at is correct goal point
                return False
        return True
    
    # This function returns a list of all the possible actions that can be applied to the given state
    def get_actions(self, state: ParkingState) -> List[ParkingAction]:
        ans = []
        for s in range(len(state)):
            #using function add to move 1 step in each direction to check if valid along with checking there is no car there
            goRight = state[s].__add__(Direction.RIGHT.to_vector()) 
            if (goRight in self.passages) and (goRight not in state): 
                ans.append((s,Direction.RIGHT))
            goLeft = state[s].__add__(Direction.LEFT.to_vector())
            if (goLeft in self.passages) and (goLeft not in state): 
                ans.append((s,Direction.LEFT))
            goUp = state[s].__add__(Direction.UP.to_vector())
            if (goUp in self.passages) and (goUp not in state): 
                ans.append((s,Direction.UP))
            goDown = state[s].__add__(Direction.DOWN.to_vector())
            if (goDown in self.passages) and (goDown not in state): 
                ans.append((s,Direction.DOWN))
        return ans
             
    
    # This function returns a new state which is the result of applying the given action to the given state
    def get_successor(self, state: ParkingState, action: ParkingAction) -> ParkingState:
        newState = state[action[0]].__add__(action[1].to_vector()) #get the new state of the car
        tempStat = list(state)                                      #make a list of the state to be able to change it
        tempStat[action[0]] = newState                              #change the state of the car
        return tuple(tempStat)
    
    # This function returns the cost of applying the given action to the given state
    def get_cost(self, state: ParkingState, action: ParkingAction) -> float:
        newPos = state[action[0]].__add__(action[1].to_vector())
        if newPos in self.slots and action[0] != self.slots.get(newPos) : #if the car is on the slot of another car
            #apply cost of 100 plus rank of car
            return (26-action[0]) + 100
        else:
            return 26-action[0] #else cost according to car rank


     # Read a parking problem from text containing a grid of tiles
    @staticmethod
    def from_text(text: str) -> 'ParkingProblem':
        passages =  set()
        cars, slots = {}, {}
        lines = [line for line in (line.strip() for line in text.splitlines()) if line]
        width, height = max(len(line) for line in lines), len(lines)
        for y, line in enumerate(lines):
            for x, char in enumerate(line):
                if char != "#":
                    passages.add(Point(x, y))
                    if char == '.':
                        pass
                    elif char in "ABCDEFGHIJ":
                        cars[ord(char) - ord('A')] = Point(x, y)
                    elif char in "0123456789":
                        slots[int(char)] = Point(x, y)
        problem = ParkingProblem()
        problem.passages = passages
        problem.cars = tuple(cars[i] for i in range(len(cars)))
        problem.slots = {position:index for index, position in slots.items()}
        problem.width = width
        problem.height = height
        return problem

    # Read a parking problem from file containing a grid of tiles
    @staticmethod
    def from_file(path: str) -> 'ParkingProblem':
        with open(path, 'r') as f:
            return ParkingProblem.from_text(f.read())
    
