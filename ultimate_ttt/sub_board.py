from copy import deepcopy

from .cell import Cell
from .gameplay import Player, PlayerMove, Move
from .gameplay import is_winning_move
from .errors import MoveOutsideSubBoardError, MoveInPlayedCellError,\
                    MoveInFinishedBoardError, BoardNotFinishedError

class SubBoard(object):
    """A single game of TicTacToe (not ultimate). Several of these make up the Ultimate TTT game.

    Instances of this class behave in a functional manner, with no method call
    modifying the state of the original object. State changing operations (such
    as :code:`add_my_move`) return a new SubBoard object, which the calling function
    must replace. The returned SubBoard object has all properties (e.g. is_finished)
    calculated.

    .. highlight:: python
    Example:
    ::
        SubBoard(3) #Initialises a board of size 3
            .add_my_move(Move(1, 1)) #Adds a move at 1, 1 and returns a SubBoard
            .add_opponent_move(Move(2, 1)) #Adds a move to the last returned board

    Call :code:`str(SubBoard())` to get a pretty-printed representation of this board

    Todo:
        * Use a :code:`@classmethod` to initialize SubBoard and make it immutable internally

    """
    def __init__(self, board_size = 3):
        if not isinstance(board_size, int) or not board_size == 3:
            raise ValueError("Size must be integer of size 3 (for now)")

        self._board_size = board_size
        self._board = [
                [Cell() for board_col in range(board_size)]
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
        if not self._is_finished:
            raise BoardNotFinishedError
        return self._winner

    def add_my_move(self, move):
        """Adds a move for the current ultimate_ttt_player

        Args:
            move: Move co-ordinates

        Returns:
            A new SubBoard instance with the move applied
        """
        return self.add_move(PlayerMove(Player.ME, move))

    def add_opponent_move(self, move):
        """Adds a move for the opponent

        Args:
            move: Move co-ordinates

        Returns:
            A new SubBoard instance with the move applied
        """
        return self.add_move(PlayerMove(Player.OPPONENT, move))

    def __str__(self):
        """Returns a pretty printed representation of this board"""
        pretty_printed = ''
        for row in self._board:
            for cell in row:
                pretty_printed += str(cell)+' '
            pretty_printed += '\n'
        return pretty_printed

    def add_move(self, player_move):
        """Adds a move by a ultimate_ttt_player to a deep copy of the board, returning the copy

        Player may find it easier to use the :code:`add_my_move` and
        :code:`add_opponent_move` convenience methods so they don't have to create
        PlayerMove objects

        Args:
            player_move: Player and intended move

        Returns:
            A new SubBoard instance with the move applied and all properties calculated
        """
        if self.is_finished == True:
            raise MoveInFinishedBoardError(player_move)

        if not(self._is_move_in_bounds(player_move)):
            raise MoveOutsideSubBoardError(player_move)

        if self._is_move_already_played(player_move):
            raise MoveInPlayedCellError(player_move)

        #Copy the board so we can update it
        #Maybe this should all go in the constructor/classmethod
        updated_sub_board = deepcopy(self)

        updated_sub_board._board[player_move.row][player_move.col] = Cell(player_move.player)
        updated_sub_board._moves_so_far += 1

        if is_winning_move(updated_sub_board._board, player_move):
            updated_sub_board._is_finished = True
            updated_sub_board._winner = player_move.player
        elif updated_sub_board._moves_so_far == updated_sub_board._max_moves:
            updated_sub_board._is_finished = True

        return updated_sub_board

    def get_valid_moves(self):
        """
        Returns:
            All valid Moves, corresponding to non-played cells in SubBoard. Empty if board is finished.
        """
        if self.is_finished:
            return []
        valid_moves = []
        for row_index in range(0, self._board_size):
            for col_index in range(0, self._board_size):
                if not self._board[row_index][col_index].is_played():
                    valid_moves.append(Move(row_index, col_index))
        return valid_moves

    ### Private functions

    def _is_move_in_bounds(self, move):
        """Checks whether the given move is inside the boundaries of this board

        Args:
            move: The intended move

        Returns:
            True if the move is within the bounds of this board, False otherwise
        """
        if (move.row >= 0 and move.row < len(self._board) and
            move.col >= 0 and move.col < len(self._board)):
            return True
        return False

    def _is_move_already_played(self, move):
        """Checks whether the given move is already played in this board

        Args:
            move: The intended move

        Returns:
            True if the cell referenced by the move is already played, False otherwise
        """
        return self._board[move.row][move.col].is_played()
