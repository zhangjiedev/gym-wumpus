import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random
from enum import Enum
class WumpusEnv(gym.Env):
    """
    Description:
        #TODO
    
    Source:
        #TODO
    
    Observation:
        Type: MultiBinary(5)
        Num	Observation        Min         Max
        0	STENCH             0           1
        1	BREEZE             0           1
        2	GLITTER            0           1
        3	BUMP               0           1
        4   SCREAM             0           1

    Actions:
        Type: Discrete(6)
        Num	Action
        0	Turn Left
        1	Turn Right
        2   Forward
        3   Shoot
        4   Grab
        5   climb
    """

    metadata = {'render.modes': ['human']}

    # Tile Structure
    class __Tile:
        pit    = False;
        wumpus = False;
        gold   = 0;
        breeze = 0;
        stench = 0;

    # Actuators
    class Action ( Enum ):
        TURN_LEFT  = 0
        TURN_RIGHT = 1
        FORWARD    = 2
        SHOOT      = 3
        GRAB       = 4
        CLIMB      = 5

    def __init__(self):
        self.action_space = spaces.Discrete(6)
        self.observation_space = spaces.MultiBinary(5)

    def step(self, action):

        self.__lastAction = self.Action(action)

        reward = -1
        done = False
        self.__bump   = 0
        self.__scream = 0
        
        if self.__lastAction == self.Action.TURN_LEFT:
            self.__agentDir -= 1
            if (self.__agentDir < 0):
                self.__agentDir = 3
                
        elif self.__lastAction == self.Action.TURN_RIGHT:
            self.__agentDir += 1
            if self.__agentDir > 3:
                self.__agentDir = 0
                
        elif self.__lastAction == self.Action.FORWARD:
            if self.__agentDir == 0 and self.__agentX+1 < self.__colDimension:
                self.__agentX += 1
            elif self.__agentDir == 1 and self.__agentY-1 >= 0:
                self.__agentY -= 1
            elif self.__agentDir == 2 and self.__agentX-1 >= 0:
                self.__agentX -= 1
            elif self.__agentDir == 3 and self.__agentY+1 < self.__rowDimension:
                self.__agentY += 1
            else:
                self.__bump = 1
                
            if self.__board[self.__agentX][self.__agentY].pit or self.__board[self.__agentX][self.__agentY].wumpus:
                reward -= 1000
                done = True
            
        elif self.__lastAction == self.Action.SHOOT:
        
            if self.__hasArrow:
                self.__hasArrow = False
                reward -= 10
                
                if self.__agentDir == 0:
                    for x in range (self.__agentX, self.__colDimension):
                            if self.__board[x][self.__agentY].wumpus:
                                self.__board[x][self.__agentY].wumpus = False
                                self.__board[x][self.__agentY].stench = 1
                                self.__scream = 1
                
                elif self.__agentDir == 1:
                    for y in range (self.__agentY, -1, -1):
                        if self.__board[self.__agentX][y].wumpus:
                            self.__board[self.__agentX][y].wumpus = False
                            self.__board[self.__agentX][y].stench = 1
                            self.__scream = True
                
                elif self.__agentDir == 2:
                    for x in range (self.__agentX, -1, -1):
                        if self.__board[x][self.__agentY].wumpus:
                            self.__board[x][self.__agentY].wumpus = False
                            self.__board[x][self.__agentY].stench = 1
                            self.__scream = 1

                elif self.__agentDir == 3:
                    for y in range (self.__agentY, self.__rowDimension):
                        if self.__board[self.__agentX][y].wumpus:
                            self.__board[self.__agentX][y].wumpus = False
                            self.__board[self.__agentX][y].stench = 1
                            self.__scream = 1
                
        elif self.__lastAction == self.Action.GRAB:
            if self.__board[self.__agentX][self.__agentY].gold:
                self.__board[self.__agentX][self.__agentY].gold = False
                self.__goldLooted = True
                
        elif self.__lastAction == self.Action.CLIMB:
            if self.__agentX == 0 and self.__agentY == 0:
                if self.__goldLooted:
                    reward += 1000
                done = True
        observation = np.array([
            self.__board[self.__agentX][self.__agentY].stench,
            self.__board[self.__agentX][self.__agentY].breeze,
            self.__board[self.__agentX][self.__agentY].gold,
            self.__bump,
            self.__scream
        ])
        self.__score += reward
        if not done:
            done = self.__score < -1000
        return (observation, reward, done, None)

    def reset(self, file=None):
        # Agent Initialization
        self.__goldLooted   = False
        self.__hasArrow     = True
        self.__bump         = 0
        self.__scream       = 0
        self.__score        = 0
        self.__agentDir     = 0
        self.__agentX       = 0
        self.__agentY       = 0
        self.__lastAction   = self.Action.CLIMB

        if file != None:
            self.__colDimension, self.__rowDimension = [int(x) for x in next(file).split()]
            self.__board = [[self.__Tile() for j in range(self.__rowDimension)] for i in range(self.__colDimension)]
            self.__addFeatures(file)
        else:
            self.__colDimension = 4
            self.__rowDimension = 4
            self.__board = [[self.__Tile() for j in range(self.__colDimension)] for i in range(self.__rowDimension)]
            self.__addFeatures()

    def render(self, mode='human'):
        pass

    def getScore(self):
        return self.__score

    def close(self):
        pass

    def __randomInt ( self, limit ):
        return random.randrange(limit)

    def __addFeatures ( self, file = None ):
        if file == None:
            # Generate pits
            for r in range (self.__rowDimension):
                for c in range (self.__colDimension):
                    if (c != 0 or r != 0) and self.__randomInt(10) < 2:
                        self.__addPit ( c, r )
            
            # Generate wumpus
            wc = self.__randomInt(self.__colDimension)
            wr = self.__randomInt(self.__rowDimension)
            
            while wc == 0 and wr == 0:
                wc = self.__randomInt(self.__colDimension)
                wr = self.__randomInt(self.__rowDimension)
                
            self.__addWumpus ( wc, wr );
            
            # Generate gold
            gc = self.__randomInt(self.__colDimension)
            gr = self.__randomInt(self.__rowDimension)
                
            while gc == 0 and gr == 0:
                gc = self.__randomInt(self.__colDimension)
                gr = self.__randomInt(self.__rowDimension)
            
            self.__addGold ( gc, gr )
            
        else:
            # Add the Wumpus
            c, r = [int(x) for x in next(file).split()]
            self.__addWumpus ( c, r )
            
            # Add the Gold
            c, r = [int(x) for x in next(file).split()]
            self.__addGold ( c, r )
            
            # Add the Pits
            numOfPits = int(next(file))
            
            while numOfPits > 0:
                numOfPits -= 1
                c, r = [int(x) for x in next(file).split()]
                self.__addPit ( c, r )
                
            file.close()
    
    def __addPit ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].pit = True
            self.__addBreeze ( c+1, r )
            self.__addBreeze ( c-1, r )
            self.__addBreeze ( c, r+1 )
            self.__addBreeze ( c, r-1 )
    
    def __addWumpus ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].wumpus = True
            self.__addStench ( c+1, r )
            self.__addStench ( c-1, r )
            self.__addStench ( c, r+1 )
            self.__addStench ( c, r-1 )
    
    def __addGold ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].gold = 1
    
    def __addStench ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].stench = 1
    
    def __addBreeze ( self, c, r ):
        if self.__isInBounds(c, r):
            self.__board[c][r].breeze = 1
    
    def __isInBounds ( self, c, r ):
        return c < self.__colDimension and r < self.__rowDimension and c >= 0 and r >= 0