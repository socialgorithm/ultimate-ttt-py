"""
A sub-board, a collection of which form the main board in a game of Ultimate
TicTacToe
"""

from copy import deepcopy

from .cell import Cell
from .gameplay import Player, PlayerMove
from .errors import MoveOutsideSubBoardError, MoveInPlayedCellError

class SubBoard(object):
    """SubBoard class"""
    def __init__(self, board_size = 3):
        if not isinstance(board_size, int) or not board_size == 3:
            raise ValueError("Size must be integer of size 3 (for now)")

        self._board = [
                [Cell() for board_col in range(board_size)]
                for board_row in range(board_size)
            ]

    def is_finished(self):
        return False

    def add_my_move(self, move):
        return self._add_move(PlayerMove(move, Player.ME))

    def add_opponent_move(self, move):
        return self._add_move(PlayerMove(move, Player.OPPONENT))

    def __str__(self):
        pretty_printed = ''
        for row in self._board:
            for cell in row:
                pretty_printed += str(cell)+' '
            pretty_printed += '\n'
        return pretty_printed

    ### Private functions

    def _add_move(self, playerMove):
        if not(self._is_move_in_bounds(playerMove)):
            raise MoveOutsideSubBoardError(playerMove)

        if self._is_move_already_played(playerMove):
            raise MoveInPlayedCellError(playerMove)

        updated_sub_board = deepcopy(self)

        updated_sub_board._board[playerMove.row][playerMove.col] = Cell(playerMove.player)

        return updated_sub_board

    def _is_move_in_bounds(self, move):
        if (move.row >= 0 and move.row < len(self._board) and
            move.col >= 0 and move.col < len(self._board)):
            return True
        return False

    def _is_move_already_played(self, move):
        return self._board[move.row][move.col].is_played()
