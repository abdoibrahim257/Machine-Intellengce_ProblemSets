from typing import Callable, DefaultDict, Dict, Generic, List, Optional, Union
from agents import Agent
from environment import Environment, S, A
from helpers.mt19937 import RandomGenerator
from helpers.utils import NotImplemented
import copy
import json
from collections import defaultdict

# The base class for all Reinforcement Learning Agents required for this problem set


class RLAgent(Agent[S, A]):
    rng: RandomGenerator  # A random number generator used for exploration
    actions: List[A]  # A list of all actions that the environment accepts
    discount_factor: float  # The discount factor "gamma"
    epsilon: float  # The exploration probability for epsilon-greedy
    learning_rate: float  # The learning rate "alpha"

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__()
        # initialize the random generator with a seed for reproducability
        self.rng = RandomGenerator(seed)
        self.actions = actions
        self.discount_factor = discount_factor
        self.epsilon = epsilon
        self.learning_rate = learning_rate

    # A virtual function that returns the Q-value for a specific state and action
    # This should be overriden by the derived RL agents
    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        return 0

    # Returns true if we should explore (rather than exploit)
    def should_explore(self) -> bool:
        return self.rng.float() < self.epsilon

    def act(self, env: Environment[S, A], observation: S, training: bool = False) -> A:
        actions = env.actions()
        if training and self.should_explore():
            # DONE: Return a random action whose index is "self.rng.int(0, len(actions)-1)"
                                                            #           /\
            return actions[self.rng.int(0, len(actions)-1)] # ==========||
        else:
            # DONE: return the action with the maximum q-value as calculated by "compute_q" above
            # if more than one action has the maximum q-value, return the one that appears first in the "actions" list
            max_q = float('-inf') #initialise the max q-value to negative infinity
            best_action = None #initialise the best action to None to be updated later
            for action in env.actions(): # iterate over all possible actions
                q = self.compute_q(env, observation, action) # compute the q-value for the given action
                if q > max_q: #maximise the q-value to return the best action
                    max_q = q
                    best_action = action
            return best_action

#############################
#######     SARSA      ######
#############################

# This is a class for a generic SARSA agent


class SARSALearningAgent(RLAgent[S, A]):
    Q: DefaultDict[S, DefaultDict[A, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(
            lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries

    # Update the value of Q(state, action) using this transition via the SARSA update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, next_action: Optional[A]):
        # DONE: Complete this function to update Q-table using the SARSA update rule
        # If next_action is None, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
                                                                                                    # /\
        if next_action is None: #if the next action is None, then the next state is a terminal state  ||
            self.Q[next_state][next_action] =0
        self.Q[state][action] += self.learning_rate * (reward + self.discount_factor * self.Q[next_state][next_action] - self.Q[state][action]) #compute SARSA update rule as given in the instructions
    
    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#############################
#####   Q-Learning     ######
#############################

# This is a class for a generic Q-learning agent


class QLearningAgent(RLAgent[S, A]):
    Q: DefaultDict[str, DefaultDict[str, float]]  # The table of the Q values
    # The first key is the string representation of the state
    # The second key is the string representation of the action
    # The value is the Q-value of the given state and action

    def __init__(self,
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        self.Q = defaultdict(lambda: defaultdict(lambda: 0))  # The default Q value is 0

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        # Return the Q-value of the given state and action
        return self.Q[state][action]
        # NOTE: we cast the state and the action to a string before querying the dictionaries

    # Given a state, compute and return the utility of the state using the function "compute_q"
    def compute_utility(self, env: Environment[S, A], state: S) -> float:
        # DONE: Complete this function.
        # Return the maximum Q-value of the given state(next state) over all possible actions as in instruction.md
        q_val = [self.compute_q(env, state, a) for a in env.actions()] #compute the q-value for each action and insert into a list
        return max(q_val) # return the maximum q-value from the previous list

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # DONE: Complete this function to update Q-table using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
        if done:                                                                                                # /\                    
            max_q = 0 # if the next state is a terminal state, then the maximum q-value is 0 =====================||
        max_q = self.compute_utility(env, next_state)  # compute the maximum q-value for the next state of each action
        self.Q[state][action] += self.learning_rate * (reward + self.discount_factor * max_q - self.Q[state][action]) # compute the Q-learning update rule as given in instruction.md

    # Save the Q-table to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            Q = {
                env.format_state(state): {
                    env.format_action(action): value for action, value in state_q.items()
                } for state, state_q in self.Q.items()
            }
            json.dump(Q, f, indent=2, sort_keys=True)

    # load the Q-table from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            Q = json.load(f)
            self.Q = {
                env.parse_state(state): {
                    env.parse_action(action): value for action, value in state_q.items()
                } for state, state_q in Q.items()
            }

#########################################
#####   Approximate Q-Learning     ######
#########################################
# The type definition for a set of features representing a state
# The key is the feature name and the value is the feature value
Features = Dict[str, float]

# This class takes a state and returns the a set of features


class FeatureExtractor(Generic[S, A]):

    # Returns a list of feature names.
    # This will be used by the Approximate Q-Learning agent to initialize its weights dictionary.
    @property
    def feature_names(self) -> List[str]:
        return []

    # Given an enviroment and an observation (a state), return a set of features that represent the given state
    def extract_features(self, env: Environment[S, A], state: S) -> Features:
        return {}

# This is a class for a generic Q-learning agent


class ApproximateQLearningAgent(RLAgent[S, A]):
    weights: Dict[A, Features]    # The weights dictionary for this agent.
    # The first key is action and the second key is the feature name
    # The value is the weight
    # The feature extractor used to extract the features corresponding to a state
    feature_extractor: FeatureExtractor[S, A]

    def __init__(self,
                 feature_extractor: FeatureExtractor[S, A],
                 actions: List[A],
                 discount_factor: float = 0.99,
                 epsilon: float = 0.5,
                 learning_rate: float = 0.01,
                 seed: Optional[int] = None) -> None:
        super().__init__(actions, discount_factor, epsilon, learning_rate, seed)
        feature_names = feature_extractor.feature_names
        self.weights = {action: {feature: 0 for feature in feature_names}
                        for action in actions}  # we initialize the weights to 0
        self.feature_extractor = feature_extractor

    # Given the features of state and an action, compute and return the Q value
    def __compute_q_from_features(self, features: Dict[str, float], action: A) -> float:
        # DONE: Complete this function
        # NOTE: Remember to cast the action to string before quering self.weights
        # compute the q-value for each feature and sum them up given an action
        return sum([features[f] * self.weights[action][f] for f in features]) # computing the q-value for each feature and summing them up

    # Given the features of a state, compute and return the utility of the state using the function "__compute_q_from_features"
    def __compute_utility_from_features(self, features: Dict[str, float]) -> float:
        # DONE: Complete this function
        q = [self.__compute_q_from_features(features, act) for act in self.actions] #get Q value for each action and insert into a list to maximize the q-value after computing q from features with the help of implemented function above
        return max(q)

    def compute_q(self, env: Environment[S, A], state: S, action: A) -> float:
        features = self.feature_extractor.extract_features(env, state)
        return self.__compute_q_from_features(features, action)

    # Update the value of Q(state, action) using this transition via the Q-Learning update rule
    def update(self, env: Environment[S, A], state: S, action: A, reward: float, next_state: S, done: bool):
        # DONE: Complete this function to update weights using the Q-Learning update rule
        # If done is True, then next_state is a terminal state in which case, we consider the Q-value of next_state to be 0
    
        maxNextQ = 0 #if the next state is a terminal state, then the maximum q-value is 0 (if done)
        copyWeights = copy.deepcopy(self.weights) #copy weights to avoid changing the original weights bacause we need the old weights to compute the new weights
        if not done: # if the next state is not a terminal state, then compute the maximum q-value for the next state
            maxNextQ = self.__compute_utility_from_features(self.feature_extractor.extract_features(env, next_state))
    
        features = self.feature_extractor.extract_features(env, state) # get the features for the current state from the computed 
        for f in features: # update the weights for each feature and action using the equation given in the instructions
            copyWeights[action][f] = self.weights[action][f] +self.learning_rate * (reward + self.discount_factor * maxNextQ - self.compute_q(env,state,action)) * features[f]
        self.weights = copyWeights # update the weights to the new weights

    # Save the weights to a json file
    def save(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'w') as f:
            weights = {env.format_action(
                action): w for action, w in self.weights.items()}
            json.dump(weights, f, indent=2, sort_keys=True)

    # load the weights from a json file
    def load(self, env: Environment[S, A], file_path: str):
        with open(file_path, 'r') as f:
            weights = json.load(f)
            self.weights = {env.parse_action(
                action): w for action, w in weights.items()}
