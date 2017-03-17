"""
Errors for the Ultimate TicTacToe Engine
"""

class Error(Exception):
    """Base class for exceptions"""
    pass

class MoveOutsideSubBoardError(Error):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return "Move ("+str(self.move.row)+","+str(self.move.col)+") made outside sub board bounds"

class MoveInPlayedCellError(Error):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return "Move ("+str(self.move.row)+","+str(self.move.col)+") made in already played cell"
