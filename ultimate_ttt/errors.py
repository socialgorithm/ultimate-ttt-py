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
        return "Co-ordinate ("+str(self.coords)+") made outside main board bounds"

class MoveNotOnNextBoardError(Error):
    def __init__(self, board_coords, next_board_coords):
        self.coords = board_coords
        self.next_board_coords = next_board_coords

    def __str__(self):
        return "Next board to play is "+self.next_board_coords+", but ultimate_ttt_player played "+self.coords

class MoveOutsideSubBoardError(Error):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return "Move ("+str(self.move.row)+","+str(self.move.col)+") made outside sub board bounds"

class MoveInPlayedCellError(Error):
    def __init__(self, move, board_coords = None):
        self.move = move
        self.board_coords = board_coords

    def __str__(self):
        msg = "Move "+str(self.move)+" made in already played cell"
        if not self.board_coords == None:
            msg += " in board "+str(self.board_coords)
        return msg

class MoveInFinishedBoardError(Error):
    def __init__(self, move):
        self.move = move

    def __str__(self):
        return "Move ("+str(self.move.row)+","+str(self.move.col)+") made in finished board"

class BoardNotFinishedError(Error):
    def __str__(self):
        return "Board is currently in play"
