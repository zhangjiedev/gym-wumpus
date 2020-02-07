import gym
import numpy as np
from gym import error, spaces, utils
from gym.utils import seeding

from game import *
REWARDS = {
    'S': 0
    'W': -1000
    'P': -1000
    'A': -1
    'S': -10
    'G': 1000
}

MAPS = None

ENDSTATES = ['w', 'P', 'G']

STARTSTATES = ['S']

# Tile Structure
class Tile(object):
    def __init__(self, states=[]):
        self.states = states
    '''    
    pit    = False;
    wumpus = False;
    gold   = False;
    breeze = False;
    stench = False;
    '''

class Agent():
    # Actuators
    @staticmethod
    class Action ( Enum ):
        TURN_LEFT  = 1
        TURN_RIGHT = 2
        FORWARD    = 3
        SHOOT      = 4
        GRAB       = 5
        CLIMB      = 6
    
    Actions = [Agent.Action(i) for i in range(1, 7)]

    def __init__(self, pos = (1, 1)):
        self.pos = pos

    def getAction ( self,
        # Sensors
        stench,
        breeze,
        glitter,
        bump,
        scream
    ):
        pass

    def getPos(self):
        return self.pos

class World():
    
    def __init__(self, seed=None):
        self.grid = np.zeros((4, 4))
        #TODO
    
    def getState(self, pos):
        if len(pos) != 2:
            raise Exception("Position format Error!")
        return self.grid[pos[0]][pos[1]]
    
    def getReward(self, state):
        #TODO
        
class GameState():

    def __init__(self):

        #Agent
        self.agent = None
        self.agentPos = None
        self.agentDir = None

        #World
        self.world = None

        #Score
        self.score = 0
    
    def generateState(self, action):
        nextState = None
        return nextState


class WumpusEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, seed=None, N=None, M=None):
        self.world = World(seed)
        

    def step(self, action):
        """ return observation, reward, done and info """
        #Generate Next State
        state = self.generateState(action)

        #Observation
        observation = self.getObservation(state)

        #Reward
        reward = self.getReward(state)

        #Done
        done = self.isTerminalState(state)

        #Info
        info = None

        return (observation, reward, done, info)

    def reset(self):
        pass

    def render(self, mode='human'):
        pass
    
    def generateState(self, action):
        """ Generate next state from current state and action. """
        #TODO

    def setState(self, state):
        #TODO
    
    def getObservation(self, state):
        """ Implementation for observation. """
        #TODO

    def getReward(self, state):
        """ Implementation for reward. """
        return self.world.getReward(state)

    def isTerminalState(self, state):
        """ Implementation for done. """
        #TODO

    def close(self):
        pass
