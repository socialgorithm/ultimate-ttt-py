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

class PlayerMove(Move):
    """A move by a specific player"""
    def __init__(self, player, move):
        super().__init__(move.row, move.col)
        self.player = player

class BoardCoords(Move):
    """Convenience wrapper to represent MainBoard co-ordinates (referencing a SubBoard)"""
    def __init__(self, main_board_row, main_board_col):
        super().__init__(main_board_row, main_board_col)

def is_winning_move(board, player_move):
    return (is_row_won(board, player_move) or is_col_won(board, player_move) or
                is_diagonal_won(board, player_move))

def is_row_won(board, player_move):
    for cell in board[player_move.row]:
        if not cell.played_by == player_move.player:
            return False
    return True

def is_col_won(board, player_move):
    for row in board:
        if not row[player_move.col].played_by == player_move.player:
            return False
    return True

def is_diagonal_won(board, player_move):
    ltr_diagonal = [[0,0],[1,1],[2,2]]
    rtl_diagonal = [[0,2],[1,1],[2,0]]

    move = [player_move.row, player_move.col]

    move_was_in_diagonal = False

    if move in ltr_diagonal:
        move_was_in_diagonal = True
        for (test_row, test_col) in ltr_diagonal:
            if not board[test_row][test_col].played_by == player_move.player:
                return False

    if move in rtl_diagonal:
        move_was_in_diagonal = True
        for (test_row, test_col) in rtl_diagonal:
            if not board[test_row][test_col].played_by == player_move.player:
                return False

    if move_was_in_diagonal:
        return True

    return False
