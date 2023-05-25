from typing import Dict, List, Optional, Set, Tuple
from mdp import MarkovDecisionProcess
from environment import Environment
from mathutils import Point, Direction
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import json
from dataclasses import dataclass

"""
Environment Description:
    The snake is a 2D grid world where the snake can move in 4 directions.
    The snake always starts at the center of the level (floor(W/2), floor(H/2)) having a length of 1 and moving LEFT.
    The snake can wrap around the grid.
    The snake can eat apples which will grow the snake by 1.
    The snake can not eat itself.
    You win if the snake body covers all of the level (there is no cell that is not occupied by the snake).
    You lose if the snake bites itself (the snake head enters a cell occupied by its body).
    The action can not move the snake in the opposite direction of its current direction.
    The action can not move the snake in the same direction 
        i.e. (if moving right don't give an action saying move right).
    Eating an apple increases the reward by 1.
    Winning the game increases the reward by 100.
    Losing the game decreases the reward by 100.
"""

# IMPORTANT: This class will be used to store an observation of the snake environment
@dataclass(frozen=True)
class SnakeObservation:
    snake: Tuple[Point]     # The points occupied by the snake body 
                            # where the head is the first point and the tail is the last  
    direction: Direction    # The direction that the snake is moving towards
    apple: Optional[Point]  # The location of the apple. If the game was already won, apple will be None


class SnakeEnv(Environment[SnakeObservation, Direction]):

    rng: RandomGenerator  # A random generator which will be used to sample apple locations

    snake: List[Point]
    direction: Direction
    apple: Optional[Point]

    def __init__(self, width: int, height: int) -> None:
        super().__init__()
        assert width > 1 or height > 1, "The world must be larger than 1x1"
        self.rng = RandomGenerator()
        self.width = width
        self.height = height
        self.snake = []
        self.direction = Direction.LEFT
        self.apple = None

    def generate_random_apple(self) -> Point:
        """
        Generates and returns a random apple position which is not on a cell occupied 
        by the snake's body.
        """
        snake_positions = set(self.snake)
        possible_points = [Point(x, y) 
            for x in range(self.width) 
            for y in range(self.height) 
            if Point(x, y) not in snake_positions
        ]
        return self.rng.choice(possible_points)

    def reset(self, seed: Optional[int] = None) -> Point:
        """
        Resets the Snake environment to its initial state and returns the starting state.
        Args:
            seed (Optional[int]): An optional integer seed for the random
            number generator used to generate the game's initial state.

        Returns:
            The starting state of the game, represented as a Point object.
        """
        if seed is not None:
            self.rng.seed(seed) # Initialize the random generator using the seed
        # DONE add your code here
        # IMPORTANT NOTE: Define the snake before calling generate_random_apple
        self.snake = [Point((int)(self.width / 2), (int)(self.height / 2))] #start at the center of the grid
        self.direction = Direction.LEFT #setting the direction to left the default direction
        self.apple = self.generate_random_apple() #generate the apple

        return SnakeObservation(tuple(self.snake), self.direction, self.apple)

    def actions(self) -> List[Direction]:
        """
        Returns a list of the possible actions that can be taken from the current state of the Snake game.
        Returns:
            A list of Directions, representing the possible actions that can be taken from the current state.

        """
        # DONE add your code here
        # a snake can wrap around the grid
        # NOTE: The action order does not matter
        #check on available actions
        available_actions = [] #list of available actions
        available_actions.append(Direction.NONE) #no action is also an action
        currPoint = self.snake[0] #get the head of the snake
        if self.direction != Direction.RIGHT and self.direction != Direction.LEFT: #check if the snake is not moving right (i cannot assign direction to left or right) and not moving left (i cannot assign direction to left or right)
                                                                                    #this condition is to prevent the snake from moving in the opposite direction ad combine both cases in one condition
                available_actions.append(Direction.RIGHT) #then add the available actions
                available_actions.append(Direction.LEFT)
        if self.direction != Direction.DOWN and self.direction != Direction.UP: # same goes here if iam moving down i cannot assign direction to up or down and vice versa then add the available actions
                available_actions.append(Direction.DOWN)
                available_actions.append(Direction.UP)

        return available_actions
    

    def step(self, action: Direction) -> \
            Tuple[SnakeObservation, float, bool, Dict]:
        """
        Updates the state of the Snake game by applying the given action.

        Args:
            action (Direction): The action to apply to the current state.

        Returns:
            A tuple containing four elements:
            - next_state (SnakeObservation): The state of the game after taking the given action.
            - reward (float): The reward obtained by taking the given action.
            - done (bool): A boolean indicating whether the episode is over.
            - info (Dict): A dictionary containing any extra information. You can keep it empty.
        """
        # DONE Complete the following function
        #first thing if iam assigned none action then do nothing
        done = False
        reward = 0
        new_head: Point

        if action != Direction.NONE: #if the action is none then the direction is tha same as the previous direction 
            self.direction = action

        new_head = self.snake[0] + self.direction.to_vector() #get the new head position in new_head variable with the help of mathUtil function to_vector
        # check on new head postion if is in range of grid and check for collision
        
        # wrapping around the grid
        if new_head.x < 0: 
            new_head = Point(self.width - 1, new_head.y) #if the new head is less than 0 then the new head is the width - 1
        elif new_head.x >= self.width:
            new_head = Point(0, new_head.y) #if the new head is greater than the width then the new head is 0

        if new_head.y < 0:
            new_head = Point(new_head.x, self.height - 1) #if the new head is less than 0 then the new head is the height - 1
        elif new_head.y >= self.height:
            new_head = Point(new_head.x, 0) #if the new head is greater than the height then the new head is 0

        self.snake.insert(0, new_head) #insert the new head to the snake list

        if new_head in self.snake[1:]: # if the new_head in the snake body part list then the snake is collided with itself
            done = True #end the game
            reward -= 100 #decrease the reward by 100
        
        if (new_head == self.apple): #if the new head is the apple
            #increase the reward by 1
            reward += 1 
            #generate a new apple only if the game is not fininshed so i need to check if the snake is full or not
            if len(self.snake) == self.width * self.height:
                done = True
                reward += 100
            else:
                self.apple = self.generate_random_apple()
        else:
            #remove the tail advancing the snake
            self.snake.pop() #remove the last element in the snake list as it is the tail moved to the next position
    

        observation = SnakeObservation(tuple(self.snake), self.direction, self.apple)
        
        return observation, reward, done, {}

    ###########################
    #### Utility Functions ####
    ###########################

    def render(self) -> None:
        # render the snake as * (where the head is an arrow < ^ > v) and the apple as $ and empty space as .
        for y in range(self.height):
            for x in range(self.width):
                p = Point(x, y)
                if p == self.snake[0]:
                    char = ">^<v"[self.direction]
                    print(char, end='')
                elif p in self.snake:
                    print('*', end='')
                elif p == self.apple:
                    print('$', end='')
                else:
                    print('.', end='')
            print()
        print()

    # Converts a string to an observation
    def parse_state(self, string: str) -> SnakeObservation:
        snake, direction, apple = eval(str)
        return SnakeObservation(
            tuple(Point(x, y) for x, y in snake), 
            self.parse_action(direction), 
            Point(*apple)
        )
    
    # Converts an observation to a string
    def format_state(self, state: SnakeObservation) -> str:
        snake = tuple(tuple(p) for p in state.snake)
        direction = self.format_action(state.direction)
        apple = tuple(state.apple)
        return str((snake, direction, apple))
    
    # Converts a string to an action
    def parse_action(self, string: str) -> Direction:
        return {
            'R': Direction.RIGHT,
            'U': Direction.UP,
            'L': Direction.LEFT,
            'D': Direction.DOWN,
            '.': Direction.NONE,
        }[string.upper()]
    
    # Converts an action to a string
    def format_action(self, action: Direction) -> str:
        return {
            Direction.RIGHT: 'R',
            Direction.UP:    'U',
            Direction.LEFT:  'L',
            Direction.DOWN:  'D',
            Direction.NONE:  '.',
        }[action]