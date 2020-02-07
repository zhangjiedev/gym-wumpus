import numpy as np
class Action ( Enum ):
        TURN_LEFT  = 1
        TURN_RIGHT = 2
        FORWARD    = 3
        SHOOT      = 4
        GRAB       = 5
        CLIMB      = 6


class GameStateData:

    def __init__(self, prevState = None):
        """
        Generates a new data packer by copying information from its predecessor.
        """

        if prevState != None:
            #TODO
            # Game
            self.score = 0
            self.lastAction = None

            # Agent
            self.agentPosition = (1, 1)


        #TODO
    
    def initialize(self, seed):
        """
        Creates an initial data packer from a seed array.
        """
        #TODO
        self.wumpus = Layout.getWumpus(seed)
        self.pitfalls = Layout.getPitfalls(seed)
        self.observation = {
            "STENCH"  = False,
            "BREEZE"  = False,
            "GLITTER" = False,
            "BUMP"    = False,
            "SCREAM"  = False
        }

class GameState:
    """
    """
    def generateSuccessor(self, action):
        #TODO
        if self.isTerminalState():
            raise Exception('Can\'t generate a successor of a terminal state.')
        
        state = GameState(self)
        Rules.applyAction(state, action)

        return state

# Agent
    def getLegalActions(self):
        #TODO

# Game
    def getScore(self):
        return self.data.score
    
    def getLastAction(self):
        return self.data.lastAction

    def isTerminalState(self):
        return Rules.isTerminate(self)


# Hidden
    def getAgentPosition(self):
        return self.data.agentPosition

    def __init__(self):
        """
        Generates a new state by copying information from its predecessor.
        """
        if prevState != None:
            #TODO
            self.data = GameStateData()
        else:
            #TODO
            self.data = GameStateData()
    
    def initialize(self, seed):
        """
        Creates an initial game state from a seed array.
        """
        self.data.initialize(seed)


class Rules:

    @staticmethod
    def isTerminate(state: GameState):
        #TODO
        if state.getScore() <= -1000:
            return True
        elif (
            state.getLastAction().value() == 6 & # Agent's last action is climb.
            state.getAgentPosition() == (0, 0)   # Agent's location is the start location.
        ):
            return True
        return False
    
    @staticmethod
    def applyAction(state, action):
        #TODO
        state.data.score -= 1

class Layout:
    """
    Generates the Map from seed.
    seed format
    [
        (size of the world),
        (the position of wumpus),
        (the position of gold),
        (the posiiton of first pitfall),
        ...
    ]
    """
    @staticmethod
    def getMap(seed):
        return seed[0]

    @staticmethod
    def getWumpus(seed):
        return seed[1]

    @staticmethod
    def getGold(seed):
        return seed[2]

    @staticmethod
    def getPitfalls(seed):
        pitfalls = np.array(seed[3:])




    
    