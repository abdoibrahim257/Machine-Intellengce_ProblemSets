# This file contains the options that you should modify to solve Question 2

def question2_1():
    #DONE: Choose options that would lead to the desired results 
    return {
        #low discount factor to make the agent care more about the immediate reward and less about the future rewards
        #  making the lliving reward small -ve to make the agent to move away bellow -ve rewards and to exit the environment soon not to stay in the environment
        "noise": 0,
        "discount_factor": 0.256,
        "living_reward": -2
    }

def question2_2():
    #DONE: Choose options that would lead to the desired results
    #low discount factor to make the agent care more about the immediate reward and less about the future rewards
    #and little noise to make disturbance in movement of the agent to make it move in a large area
    #and making the lliving reward small -2 to make the agennt to move away bellow -10 rewards and to exit the environment soon not to stay in the environment
    return {
        "noise": 0.2,
        "discount_factor": 0.256,
        "living_reward": -2
    }

def question2_3():
    #DONE: Choose options that would lead to the desired results
    return {
        #high discount factor to make the agent care more about the future rewards and less about the immediate reward
        #and making the lliving reward small -2 to make the agennt to move away bellow -10 rewards and to exit the environment soon not to stay in the environment
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -2
    }

def question2_4():
    #DONE: Choose options that would lead to the desired results
        return {
        #high discount factor to make the agent care more about the future rewards and very small small living reward to make the agent to move away from short distance
        # and little noise to make disturbance in movement of the agent to make it move in a large area and to exit the environment soon
        # making living reward very small to make agent roam around the environment (seeking long distance) and to exit the environment 
        "noise": 0.15,
        "discount_factor": 1,
        "living_reward": -0.0142369
    }

def question2_5():
    #DONE: Choose options that would lead to the desired results
    return {
        #to stay longer in the environment which is foreever, the agent should have a high living reward to stay in the environment
        "noise": 0,
        "discount_factor": 1,
        "living_reward": 150
    }

def question2_6():
    #DONE: Choose options that would lead to the desired results
    return {
        #to make the agent finish as fast as possible, the agent should have a very small negative living reward to gor to -10 faster a value smaaller than terminal state -10
        "noise": 0,
        "discount_factor": 1,
        "living_reward": -150
    }