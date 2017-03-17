from enum import Enum

class Player(Enum):
    """Identifiers for players"""
    NONE = 0
    ME = 1
    ONE = 1
    OPPONENT = 2
    TWO = 2

class Move(object):
    """Move co-ordinates"""
    def __init__(self, row, col):
        self.row = row
        self.col = col

class PlayerMove(Move):
    """A move by a specific player"""
    def __init__(self, move, player):
        self.row = move.row
        self.col = move.col
        self.player = player
