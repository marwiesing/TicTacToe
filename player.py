from enum import Enum

class Player(Enum):
    UNOCCUPIED = 0
    PLAYER_X = 1
    PLAYER_O = 2

class WINNER(Enum):
    DRAW = 0
    PLAYER_X = 1
    PLAYER_O = 2
