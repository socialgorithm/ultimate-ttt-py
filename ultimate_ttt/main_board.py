from copy import deepcopy

from .sub_board import SubBoard
from .gameplay import Player, PlayerMove
from .errors import MoveOutsideMainBoardError

class MainBoard(object):
    """An Ultimate TicTacToe board, containing several SubBoards where players play

    When the board size is 3, the main board looks like this:

    | SubBoard 0,0 | SubBoard 0,1 | SubBoard 0,2 |
    | SubBoard 1,0 | SubBoard 1,1 | SubBoard 1,2 |
    | SubBoard 2,0 | SubBoard 2,1 | SubBoard 2,2 |

    Each SubBoard looks like this:

    | Cell 0,0 | Cell 0,1 | Cell 0,2 |
    | Cell 1,0 | Cell 1,1 | Cell 1,2 |
    | Cell 2,0 | Cell 2,1 | Cell 2,2 |

    """

    def __init__(self, board_size = 3):
        if not isinstance(board_size, int) or not board_size == 3:
            raise ValueError("Size must be integer of size 3 (for now)")

        self._board = [
                [SubBoard() for board_col in range(board_size)]
                for board_row in range(board_size)
            ]

        self._max_moves = board_size * board_size;
        self._moves_so_far = 0
        self._is_finished = False
        self._winner = Player.NONE

    @property
    def is_finished(self):
        """Whether the board is finished (tied, won or lost)"""
        return self._is_finished

    @property
    def winner(self):
        """The winner of the board if finished. Exception otherwise"""
        if not self.is_finished:
            raise BoardNotFinishedError
        return self._winner

    def add_my_move(self, board_coords, move):
        """Adds your move to the specified sub-board

        Args:
            board_coords: The co-ordinates (row, column) of the SubBoard to play on
            move: The move (row, column) to make on the SubBoard

        Returns:
            A new MainBoard instance with the move applied
        """
        return self._add_move(board_coords, PlayerMove(Player.ME, move))

    def add_opponent_move(self, board_coords, move):
        """Adds the opponent's move to the specified sub-board

        Args:
            board_coords: The co-ordinates (row, column) of the SubBoard to play on
            move: The move (row, column) to make on the SubBoard

        Returns:
            A new MainBoard instance with the move applied
        """
        return self._add_move(board_coords, PlayerMove(Player.OPPONENT, move))

    def __str__(self):
        """Returns a pretty printed representation of the main board"""
        pretty_printed = ''
        for row in self._board:
            for cell in row:
                pretty_printed += str(cell)+' '
            pretty_printed += '\n'
        return pretty_printed

    ### Private functions

    def _add_move(self, board_coords, player_move):
        """Adds a move by a player to a deep copy of the current board, returning the copy

        Args:
            player_main_board_move: Player, co-ordinates of the SubBoard, and intended move on that SubBoard

        Returns:
            A new MainBoard instance with the move applied and all properties calculated
        """
        if not(self._is_board_in_bounds(board_coords)):
            raise MoveOutsideMainBoardError(board_coords)

        #Apply the move the sub board first to ensure it works
        updated_sub_board = self._board[board_coords.row][board_coords.col]\
                                .add_move(player_move)

        #Copy the board so we can update it
        #Maybe this should all go in the constructor/classmethod
        updated_main_board = deepcopy(self)

        updated_main_board._board[player_main_board_move.row][player_main_board_move.col] = updated_sub_board
        updated_main_board._moves_so_far += 1

#        if is_winning_move(updated_sub_board._board, player_main_board_move):
#            updated_sub_board._is_finished = True
#            updated_sub_board._winner = player_main_board_move.player
#        elif updated_sub_board._moves_so_far == updated_sub_board._max_moves:
#            updated_sub_board.is_finished = True

        return updated_main_board

    def _is_board_in_bounds(self, coords):
        """Checks whether the given move is inside the boundaries of the main board

        Args:
            coords: The coords of the intended sub-board

        Returns:
            True if the move is within the bounds of the main board, False otherwise
        """

        if (coords.row >= 0 and coords.row < len(self._board) and
            coords.col >= 0 and coords.col < len(self._board)):
            return True
        return False
