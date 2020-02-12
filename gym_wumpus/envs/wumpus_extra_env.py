import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
import random
from enum import Enum

class WumpusExtraEnv(gym.Env):
    """
    Description:
        #TODO
    
    Source:
        #TODO
    
    Observation:
        Type: Box(6) change to MultiBinary(6)
        Num	Observation        Min         Max
        0	STENCH             0           1
        1	BREEZE             0           1
        2	GLITTER            0           1
        3	BUMP               0           1
        4   SCREAM             0           1
        5   LocationX          0           10 (removed)
        6   LocationY          0           6  (removed)
        5   ForwardLoc Visited 0           1
        6   Has Arrow          0           1  (removed)
        6   Score              -2000       1000


    Actions:
        Type: Discrete(6)
        Num	Action
        0	Turn Left
        1	Turn Right
        2   Forward
        3   Shoot
        4   Grab (removed)
        4   EXIT
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
        visit  = 0

    # Actuators
    class Action ( Enum ):
        TURN_LEFT  = 0
        TURN_RIGHT = 1
        FORWARD    = 2
        SHOOT      = 3
        #GRAB       = 4 (removed)
        EXIT       = 4
        CLIMB      = 5

    def __init__(self):
        self.action_space = spaces.Discrete(6)
        #self.observation_space = spaces.Box(low=np.array([0, 0, 0, 0, 0, 0, -2000]), high=np.array([2, 2, 2, 2, 2, 2, 1001]), dtype=np.int16)
        self.observation_space = spaces.MultiBinary(7)

    def step(self, action):

        self.__lastAction = self.Action(action)
        # Easy Env Implementation
        reward = -1
        #reward = 0
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
            x, y = self.__getForwardLocation()
            if (x, y) == (self.__agentX, self.__agentY):
                self.__bump = 1
            else:
                self.__agentX, self.__agentY = x, y
                # Easy Env Implementation
                if not self.__board[x][y].visit:
                    #reward += 1
                    self.__board[self.__agentX][self.__agentY].visit = 1
            
            if self.__board[self.__agentX][self.__agentY].pit or self.__board[self.__agentX][self.__agentY].wumpus:
                reward -= 960
                done = True
            # Easy Env Implementation
            elif self.__board[self.__agentX][self.__agentY].gold:
                self.__board[self.__agentX][self.__agentY].gold = False
                self.__goldLooted = True
                reward += 1000
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
                
        #elif self.__lastAction == self.Action.GRAB:
            #if self.__board[self.__agentX][self.__agentY].gold:
                #self.__board[self.__agentX][self.__agentY].gold = False
                #self.__goldLooted = True
                # Easy Env Implementation
                #reward += 500
        
        elif self.__lastAction == self.Action.EXIT:
            reward -= abs(self.__score)
            done = True
                
        elif self.__lastAction == self.Action.CLIMB:
            if self.__agentX == 0 and self.__agentY == 0:
                if self.__goldLooted:
                    # Easy Env Implementation
                    #reward += 200
                    pass
                done = True

        if self.__score < -40:
            reward -= 1000

        observation = self.getObservation()
        self.__score += reward
        if not done:
            done = self.__score < -1000
        return (observation, reward, done, dict())

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
        
        self.__board[self.__agentX][self.__agentY].visit = 1
        return self.getObservation()

    def render(self, mode='human'):
        pass

    def close(self):
        pass

    def getScore(self):
        return self.__score
    
    def getObservation(self):
        x, y = self.__getForwardLocation()
        s = 1 if self.__score < -40 else 0
        return np.array([
            self.__board[self.__agentX][self.__agentY].stench,
            self.__board[self.__agentX][self.__agentY].breeze,
            self.__board[self.__agentX][self.__agentY].gold,
            self.__bump,
            self.__scream,
            self.__board[x][y].visit,
            #self.__hasArrow,
            s
        ])

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
    
    def __getForwardLocation(self):
        if self.__agentDir == 0 and self.__agentX+1 < self.__colDimension:
            return self.__agentX + 1, self.__agentY
        elif self.__agentDir == 1 and self.__agentY-1 >= 0:
            return self.__agentX, self.__agentY - 1
        elif self.__agentDir == 2 and self.__agentX-1 >= 0:
            return self.__agentX - 1, self.__agentY
        elif self.__agentDir == 3 and self.__agentY+1 < self.__rowDimension:
            return self.__agentX, self.__agentY + 1
        else:
            return self.__agentX, self.__agentY