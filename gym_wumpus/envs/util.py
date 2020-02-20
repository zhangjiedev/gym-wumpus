from gym.spaces import Dict, Box, Tuple, MultiBinary
from enum import Enum
import numpy as np

class Observation(Dict):
    """
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
    
        Type: Dict(
            'grid': info of the surrounding tiles.
            'Completeness': wheather all safy tiles are visitted.
        )
    """

    def __init__(self, x, y):
        grid = {
            (x, y): ObservationTile()
        }
        obdict = {
            'Grid': Dict(grid),
            'Completeness': MultiBinary(1)
        }
        super().__init__(obdict)
        

class ObservationTile(MultiBinary):
    """
    ObservationTile:
        Type: Box(6)
        Num	Observation        Min         Max
        0	STENCH             0           1
        1	BREEZE             0           1
        2	GLITTER            0           1
        3	BUMP               0           1
        4   SCREAM             0           1
        5   Risk               0.0         1.0
    """
    def __init__(self, sensors=np.zeros(7)):
        """
        Sensors:
            Type: np.array(7)
            Num	Observation        Min         Max
            0	STENCH             0           1
            1	BREEZE             0           1
            2	GLITTER            0           1
            3	BUMP               0           1   r
            4   SCREAM             0           1   r
            5   PIT                0.0         1.0 r
            6   WUMPUS             0.0         1.0 r
        """
        super().__init__(4)
        self.stench = sensors[0]
        self.breeze = sensors[1]
        self.gold   = sensors[2]
        self.bump   = sensors[3]
        self.scream = sensors[4]

sp = Observation(1, 1)