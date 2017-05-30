from enum import Enum

class Player(Enum):
    """Identifiers for players"""
    NONE = 0
    ME = 1
    ONE = 1
    OPPONENT = 2
    TWO = 2

class Move(object):
    """Move co-ordinates (in a SubBoard)"""
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return not(other == None) and \
            self.row == other.row and self.col == other.col

    def __ne__(self, other):
        return not self == other

    def __str__(self):
        return "("+str(self.row)+","+str(self.col)+")"

class PlayerMove(Move):
    """A move by a specific player"""
    def __init__(self, player, move):
        super().__init__(move.row, move.col)
        self.player = player

    def __str__(self):
        return "("+str(self.row)+","+str(self.col)+")"+" by "+str(self.player)

class BoardCoords(Move):
    """Convenience wrapper to represent MainBoard co-ordinates (referencing a SubBoard)"""
    def __init__(self, main_board_row, main_board_col):
        super().__init__(main_board_row, main_board_col)

def is_winning_move(board, player_move):
    """Whether the given player move is a winning move"""
    return (is_row_won(board, player_move) or is_col_won(board, player_move) or
                is_diagonal_won(board, player_move))

def is_row_won(board, player_move):
    """Whether the row of the player move is won by the player of the move"""
    return is_cell_range_played_by(board[player_move.row], player_move.player)

def is_col_won(board, player_move):
    """Whether the column of the player move is won by the player of the move"""
    for row in board:
        if not row[player_move.col].played_by == player_move.player:
            return False
    return True

def is_diagonal_won(board, player_move):
    """Whether either diagonal from the cell of the player move is won by the player"""

    return is_ltr_diagonal_won(board, player_move) or is_rtl_diagonal_won(board, player_move)

def is_ltr_diagonal_won(board, player_move):
    """Whether the left to right (0,0) to (2,2) diagonal has been won by the given player"""
    cells = [board[0][0],board[1][1],board[2][2]]

    return is_cell_range_played_by(cells, player_move.player)

def is_rtl_diagonal_won(board, player_move):
    """Whether the left to right (2,0) to (0,2) diagonal has been won by the given player"""
    cells = [board[2][0],board[1][1],board[0][2]]

    return is_cell_range_played_by(cells, player_move.player)

def is_cell_range_played_by(cells, player):
    """Whether the given list of cells are all played by the given player

    Args:
        cells: The list of cells to check
        player: The player to look for
    """
    if any(not cell.played_by == player for cell in cells):
        return False
    return True
