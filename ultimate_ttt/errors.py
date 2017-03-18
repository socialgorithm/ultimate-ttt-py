"""
Errors for the Ultimate TicTacToe Engine
"""

class Error(Exception):
    """Base class for exceptions"""
    pass

class MoveOutsideMainBoardError(Error):
    def __init__(self, board_coords):
        self.coords = board_coords

    def __str__(self):
        return "Co-ordinate ("+str(self.coords.row)+","+str(self.coords.col)+") made outside main board bounds"

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

class MoveInFinishedBoardError(Error):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return "Move ("+str(self.move.row)+","+str(self.move.col)+") made in finished board"

class BoardNotFinishedError(Error):
    def __str__(self):
        return "Board is currently in play"
